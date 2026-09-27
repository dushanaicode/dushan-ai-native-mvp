from unittest.mock import AsyncMock
from uuid import uuid4

import pymysql
import pytest
import pytest_asyncio
from httpx import URL, ASGITransport, AsyncClient

from framework.starter_security.public import SecurityRealm, SecurityService
from framework.starter_web.public import RoutePolicy
from module_system.definitions.constants.error_code_constants import ErrorCodeConstants
from module_system.framework.sms.client.providers.aliyun_sms_client import AliyunSmsClient
from module_system.framework.sms.enums.sms_template_audit_status_enum import (
    SmsTemplateAuditStatusEnum,
)
from module_system.framework.sms.factory.sms_client_factory import SmsClientFactory
from module_system.framework.sms.model.sms_template_resp_dto import SmsTemplateRespDTO
from module_system.mq.producer.sms.sms_producer import SmsProducer
from module_system.service.sms.sms_template_service import SmsTemplateService

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def call(client, method, path, **kwargs):
    result = (await client.request(method, "/admin-api/system/" + path, **kwargs)).json()
    assert result["code"] == 0, result
    return result["data"]


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def channels(admin_client):
    rows = []
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(
            AliyunSmsClient,
            "get_sms_template",
            AsyncMock(
                return_value=SmsTemplateRespDTO(
                    id="approved",
                    audit_status=SmsTemplateAuditStatusEnum.SUCCESS.code,
                )
            ),
        )
        for label in ("A", "B"):
            channel = await call(
                admin_client,
                "POST",
                "sms/channel/create",
                json={
                    "signature": label,
                    "code": "ALIYUN",
                    "status": 1,
                    "apiKey": "fixture-" + label,
                    "apiSecret": "fixture-secret-" + label,
                },
            )
            payload = {
                "type": 1,
                "status": 1,
                "code": "fixture_" + uuid4().hex[:12],
                "name": label,
                "content": label + " {code}",
                "apiTemplateId": "approved-" + label,
                "channelId": channel,
            }
            template = await call(admin_client, "POST", "sms/template/create", json=payload)
            rows.append({"channel": channel, "template": template, "payload": payload})
        yield rows


async def test_template_codes_are_global_and_channel_foreign_keys_are_enforced(
    admin_client, system_database, channels
):
    first, second = channels
    page = await call(admin_client, "GET", "sms/template/page", params={"page": 1, "pageSize": 100})
    assert {first["template"], second["template"]} <= {row["id"] for row in page["items"]}
    duplicate = (
        await admin_client.post(
            "/admin-api/system/sms/template/create",
            json={
                **first["payload"],
                "channelId": second["channel"],
            },
        )
    ).json()
    assert duplicate["code"] == ErrorCodeConstants.SMS_TEMPLATE_CODE_DUPLICATE.code
    with system_database[2].cursor() as cursor:
        with pytest.raises(pymysql.err.IntegrityError) as error:
            cursor.execute(
                "UPDATE system_sms_template SET channel_id=%s WHERE id=%s",
                (2**63 - 1, first["template"]),
            )
        assert error.value.args[0] == 1452
    temporary = {**first["payload"], "code": "reusable_" + uuid4().hex[:8]}
    old = await call(admin_client, "POST", "sms/template/create", json=temporary)
    await call(admin_client, "DELETE", "sms/template/delete", params={"id": old})
    assert await call(admin_client, "POST", "sms/template/create", json=temporary) != old


async def test_template_cache_keeps_distinct_codes_and_refreshes_status(
    system_app, admin_client, channels
):
    application = system_app.state.application_context

    async def read(row):
        with application.execution(), system_app.state.database.scope():
            async with application.container.get(SecurityService).authorized(
                admin_client.headers["Authorization"].removeprefix("Bearer "),
                RoutePolicy(realm=SecurityRealm.ACCOUNT),
            ):
                return await application.container.get(
                    SmsTemplateService
                ).get_sms_template_by_code_from_cache(row["payload"]["code"])

    for row in channels:
        assert (await read(row)).id == int(row["template"])
    first, second = channels
    await call(
        admin_client,
        "PUT",
        "sms/template/update-status",
        json={"id": first["template"], "status": 0},
    )
    try:
        assert (await read(first)).status == 0
        assert (await read(second)).status == 1
    finally:
        await call(
            admin_client,
            "PUT",
            "sms/template/update-status",
            json={"id": first["template"], "status": 1},
        )


async def test_signed_callback_is_bound_to_channel_and_log(
    system_app, system_database, admin_client, channels, monkeypatch
):
    producer = AsyncMock()
    monkeypatch.setattr(SmsProducer, "send_sms_message", producer)
    urls, logs = [], []
    for row in channels:
        urls.append(
            await call(
                admin_client, "GET", "sms/channel/callback-url", params={"id": row["channel"]}
            )
        )
        assert set(URL(urls[-1]).params) == {"token"}
        logs.append(
            await call(
                admin_client,
                "POST",
                "sms/template/send-sms",
                json={
                    "mobile": "13800138000",
                    "templateCode": row["payload"]["code"],
                    "templateParams": {"code": "1234"},
                },
            )
        )
    assert producer.await_count == 2
    with system_app.state.application_context.execution():
        factory = system_app.state.application_context.container.get(SmsClientFactory)
        await factory.close()
        factory.channel_id_clients.clear()

    def body(identifier):
        return [
            {
                "success": True,
                "err_code": "DELIVERED",
                "err_msg": "ok",
                "phone_number": "13800138000",
                "report_time": "2026-09-27T00:00:00",
                "biz_id": "fixture",
                "out_id": identifier,
            }
        ]

    async with AsyncClient(
        transport=ASGITransport(app=system_app), base_url="http://testserver"
    ) as client:
        token = URL(urls[0]).params["token"]
        invalid = token[:-1] + ("0" if token[-1] != "0" else "1")
        for url in (
            URL(urls[0]).copy_set_param("channelId", channels[1]["channel"]),
            URL(urls[0]).copy_set_param("token", invalid),
            URL(urls[1]),
        ):
            assert (await client.post(url, json=body(logs[0]))).json()["code"] != 0
        for url, identifier in zip(urls, logs, strict=True):
            assert (await client.post(url, json=body(identifier))).json()["code"] == 0
            assert (await client.post(url, json=body(identifier))).json()["code"] == 0
    with system_database[2].cursor() as cursor:
        cursor.execute(
            "SELECT channel_id,receive_status FROM system_sms_log WHERE id IN (%s,%s) ORDER BY id",
            logs,
        )
        assert cursor.fetchall() == tuple((int(row["channel"]), 10) for row in channels)
