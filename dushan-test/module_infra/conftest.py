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
def infra_database():
    with module_database("infra") as case:
        yield case


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def infra_app(infra_database, tmp_path_factory):
    from server.starter_server import create_app

    resources, name, _ = infra_database
    values = ConfigFactory.values()
    folder = tmp_path_factory.mktemp("infra-config")
    values["modules"]["enabled"] = ["framework", "system", "infra"]
    values["server"]["reload"] = False
    values["log"]["enable_file_overall"] = False
    values["log"]["console_level"] = "WARNING"
    models = values["config"]["models"]
    models["database"].update(
        enabled=True,
        health_check_enabled=False,
        id_strategy="snowflake",
        snowflake_machine_id=923,
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
        clients=[{"name": "default", "db": 11}],
    )
    models["security"].update(enabled=True, permission_cache_enabled=True, bizlog_enabled=True)
    values["expression"]["enabled"] = True
    models["data_permission"].update(enabled=True, cache_enabled=True)
    models["protection"]["enabled"] = True
    models["system"].update(
        user_register_enabled=True,
        workload_credential=uuid4().hex + uuid4().hex,
        message_signing_key=uuid4().hex + uuid4().hex,
        refresh_cookie_secure=False,
        allowed_origins=["http://testserver"],
    )
    models["job"].update(
        enabled=True, owner_enabled=True, poll_seconds=0.05, reconciliation_seconds=0.2
    )
    models["mq"].update(enabled=True, signing_secret=uuid4().hex + uuid4().hex)
    models["websocket"].update(
        enabled=True,
        signing_secret=uuid4().hex + uuid4().hex,
        allowed_origins=["http://testserver"],
    )
    models["infra_backup"].update(
        enabled=True,
        executable="C:/Program Files/MySQL/MySQL Server 8.4/bin/mysqldump.exe",
        output_directory=str(folder / "Temp/backups"),
    )
    values["config"]["reload_enabled"] = True
    values["page"]["fetch_all_enabled"] = True
    (folder / "application.yaml").write_text(
        yaml.safe_dump(values, allow_unicode=True), encoding="utf-8"
    )
    app = create_app(base_dir=folder, app_env="dev", environ={})
    app.add_middleware(HttpRouteCoverage)
    async with app.router.lifespan_context(app):
        HttpRouteCoverage.register(app)
        yield app


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def admin_client(infra_app):
    async with AsyncClient(
        transport=ASGITransport(app=infra_app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as client:
        response = (
            await client.post(
                "/admin-api/system/auth/login",
                json={"username": "admin", "password": "admin123"},
            )
        ).json()
        assert response["code"] == 0, response
        client.headers["Authorization"] = "Bearer " + response["data"]["accessToken"]
        yield client
