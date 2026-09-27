import pytest
from httpx import ASGITransport, AsyncClient

from framework.starter_database.public import AuthenticationReader
from framework.starter_security.public import OpaqueToken, SecuritySettings
from module_system.dal.dataobject.oauth2.oauth2_access_token_do import OAuth2AccessTokenDO

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_login_refresh_logout_and_application_binding(system_app, admin_client):
    async with AsyncClient(
        transport=ASGITransport(app=system_app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as client:
        login = (
            await client.post(
                "/admin-api/system/auth/login",
                json={
                    "username": "admin",
                    "password": "admin123",
                },
            )
        ).json()
        assert login["code"] == 0, login
        assert "tenantId" not in login["data"]
        token = login["data"]["accessToken"]
        client.headers["Authorization"] = "Bearer " + token
        info = (await client.get("/admin-api/system/auth/get-permission-info")).json()
        assert info["code"] == 0 and "tenantId" not in info["data"]
        with system_app.state.application_context.execution():
            settings = system_app.state.application_context.container.get(SecuritySettings)
            assert not await AuthenticationReader.token_exists(
                system_app.state.database,
                OAuth2AccessTokenDO,
                token_digest=OpaqueToken.digest(token),
                application_id=settings.application_id,
                domain="another-domain",
            )
        refreshed = (await client.post("/admin-api/system/auth/refresh-token")).json()
        assert refreshed["code"] == 0, refreshed
        assert refreshed["data"]["accessToken"] != token
        client.headers["Authorization"] = "Bearer " + refreshed["data"]["accessToken"]
        assert (await client.get("/admin-api/system/auth/get-permission-info")).json()["code"] == 0
        assert (await client.post("/admin-api/system/auth/logout")).json()["code"] == 0
        assert (await client.get("/admin-api/system/auth/get-permission-info")).json()["code"] != 0
        assert (await admin_client.get("/admin-api/system/auth/get-permission-info")).json()[
            "code"
        ] == 0


async def test_removed_tenant_routes_and_wrong_origin_cannot_start_session(system_app):
    async with AsyncClient(
        transport=ASGITransport(app=system_app), base_url="http://testserver"
    ) as client:
        for path in ("/admin-api/system/auth/tenants", "/admin-api/system/tenant/page"):
            assert (await client.get(path)).json()["code"] == 404
        response = await client.post(
            "/admin-api/system/auth/login",
            json={
                "username": "admin",
                "password": "admin123",
            },
            headers={"Origin": "https://untrusted.example"},
        )
        assert response.json()["code"] != 0
        assert not client.cookies
