from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def created(client, path, data):
    result = (await client.post("/admin-api/system/" + path, json=data)).json()
    assert result["code"] == 0, result
    return result["data"]


async def signed_in(app, username, password):
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")
    result = (
        await client.post(
            "/admin-api/system/auth/login",
            json={"username": username, "password": password},
            headers={"Origin": "http://testserver"},
        )
    ).json()
    assert result["code"] == 0, result
    client.headers["Authorization"] = "Bearer " + result["data"]["accessToken"]
    return client


async def test_owner_permissions_are_explicit_and_owner_cannot_be_disabled(
    admin_client, system_database
):
    response = (await admin_client.get("/admin-api/system/auth/get-permission-info")).json()
    assert "super_admin" in response["data"]["roles"]
    assert "system:permission:menu:create" in response["data"]["permissions"]
    assert (
        await admin_client.put(
            "/admin-api/system/user/update-status", json={"id": "10100000010001", "status": 0}
        )
    ).json()["code"] != 0
    assert (
        await admin_client.delete("/admin-api/system/user/delete", params={"id": "10100000010001"})
    ).json()["code"] != 0


async def test_legacy_super_role_binding_does_not_make_another_owner(
    admin_client, system_app, system_database
):
    username = "nonowner" + uuid4().hex[:8]
    user_id = await created(
        admin_client,
        "user/create",
        {"username": username, "nickname": "NotOwner", "password": "NotOwner123!"},
    )
    with system_database[2].cursor() as cursor:
        cursor.execute("SELECT id FROM system_role WHERE code='super_admin' AND deleted=0")
        root_role = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO system_user_role (id,user_id,role_id,creator,updater,create_time,update_time,deleted) VALUES (%s,%s,%s,'test','test',NOW(),NOW(),0)",
            (900000000000000111, user_id, root_role),
        )
    client = await signed_in(system_app, username, "NotOwner123!")
    try:
        info = (await client.get("/admin-api/system/auth/get-permission-info")).json()
        assert info["code"] == 0, info
        assert "super_admin" not in info["data"]["roles"]
        assert "*:*:*" not in info["data"]["permissions"]
        denied = (
            await client.get(
                "/admin-api/system/permission/menu/list", params={"page": 1, "pageSize": 20}
            )
        ).json()
        assert denied["code"] != 0
    finally:
        await client.aclose()
