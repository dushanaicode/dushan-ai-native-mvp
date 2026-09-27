from urllib.parse import quote
from uuid import uuid4

import pytest
import pytest_asyncio
import yaml
from httpx import ASGITransport, AsyncClient

from fixtures.config_factory import ConfigFactory
from fixtures.http_route_coverage import HttpRouteCoverage
from fixtures.module_database import module_database


@pytest.fixture(scope="module")
def system_database():
    with module_database("system") as case:
        yield case


@pytest.fixture(scope="module")
def sms_captcha_overrides():
    return {}


@pytest.fixture(scope="module")
def user_register_enabled():
    return True


@pytest.fixture(scope="module")
def auth_enabled():
    return False


@pytest.fixture(scope="module", params=[True])
def qr_login_enabled(request):
    return request.param


@pytest.fixture(scope="module")
def system_routers():
    return ()


@pytest.fixture(scope="module")
def system_allowed_origins():
    return ["http://testserver"]


@pytest.fixture(scope="module")
def system_settings_overrides():
    return {}


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def system_app(
    system_database,
    tmp_path_factory,
    sms_captcha_overrides,
    system_routers,
    system_allowed_origins,
    system_settings_overrides,
    user_register_enabled,
    auth_enabled,
    qr_login_enabled,
):
    from server.starter_server import create_app

    resources, name, _ = system_database
    values = ConfigFactory.values()
    folder = tmp_path_factory.mktemp("system-config")
    values["modules"]["enabled"] = ["framework", "system"]
    values["server"]["reload"] = False
    values["log"]["enable_file_overall"] = False
    values["log"]["console_level"] = "WARNING"
    models = values["config"]["models"]
    models["sms_captcha"].update(sms_captcha_overrides)
    models["auth"]["enabled"] = auth_enabled
    models["qr_login"]["enabled"] = qr_login_enabled
    models["database"].update(
        enabled=True,
        health_check_enabled=False,
        id_strategy="snowflake",
        snowflake_machine_id=913,
        sources=[
            dict(
                name="primary",
                url=f"mysql+aiomysql://root:{quote(resources['mysql']['root_password'])}@127.0.0.1:{resources['mysql']['port']}/{name}?charset=utf8mb4",
                role="primary",
                pool=None,
                tls=None,
            )
        ],
    )
    models["cache"].update(
        enabled=True,
        host="127.0.0.1",
        port=resources["redis"]["port"],
        password=resources["redis"]["password"],
        clients=[{"name": "default", "db": 10}],
    )
    models["security"].update(enabled=True, permission_cache_enabled=True, bizlog_enabled=True)
    values["expression"]["enabled"] = True
    models["data_permission"].update(enabled=True, cache_enabled=True)
    models["protection"]["enabled"] = True
    models["system"].update(
        user_register_enabled=user_register_enabled,
        workload_credential=uuid4().hex + uuid4().hex,
        message_signing_key=uuid4().hex + uuid4().hex,
        sms_callback_token=uuid4().hex + uuid4().hex,
        refresh_cookie_secure=False,
        allowed_origins=system_allowed_origins,
    )
    models["system"].update(system_settings_overrides)
    values["page"]["fetch_all_enabled"] = True
    (folder / "application.yaml").write_text(
        yaml.safe_dump(values, allow_unicode=True), encoding="utf-8"
    )
    app = create_app(base_dir=folder, app_env="dev", environ={}, routers=system_routers)
    app.add_middleware(HttpRouteCoverage)
    async with app.router.lifespan_context(app):
        HttpRouteCoverage.register(app)
        yield app


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def admin_client(system_app):
    async with AsyncClient(
        transport=ASGITransport(app=system_app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as client:
        result = (
            await client.post(
                "/admin-api/system/auth/login",
                json={"username": "admin", "password": "admin123"},
            )
        ).json()
        assert result["code"] == 0, result
        client.headers["Authorization"] = "Bearer " + result["data"]["accessToken"]
        yield client
