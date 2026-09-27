"""业务集成用例只连接显式登记的隔离 Docker 实例，每个模块使用独立数据库。"""

import json
import os
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

import bcrypt
import pymysql
import pytest
from pymysql.constants import CLIENT
from redis import Redis
from sqlalchemy.engine import URL


def mysql_url(resources, database):
    mysql = resources["mysql"]
    return URL.create(
        "mysql+aiomysql",
        username="root",
        password=mysql["root_password"],
        host=mysql["host"],
        port=mysql["port"],
        database=database,
        query={"charset": "utf8mb4"},
    ).render_as_string(hide_password=False)


@contextmanager
def module_database(part):
    root = Path(__file__).resolve().parents[2]
    resource_file = os.environ.get("DUSHAN_TEST_RESOURCES")
    if resource_file is None:
        pytest.skip("需要 DUSHAN_TEST_RESOURCES 指定隔离 Docker 资源清单")
    path = Path(resource_file).resolve()
    assert path.is_relative_to(root / "Temp")
    resources = json.loads(path.read_text(encoding="utf-8"))
    mysql, redis = resources["mysql"], resources["redis"]
    connection = pymysql.connect(
        host=mysql["host"],
        port=mysql["port"],
        user="root",
        password=mysql["root_password"],
        autocommit=True,
        charset="utf8mb4",
        client_flag=CLIENT.MULTI_STATEMENTS,
    )
    name = part + "_" + uuid4().hex
    db = 10 if part == "system" else 11
    cache = Redis(host=redis["host"], port=redis["port"], password=redis["password"], db=db)
    cache_owned = database_created = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@server_uuid")
            assert cursor.fetchone()[0] == mysql["server_uuid"]
            assert cache.info("server")["run_id"] == redis["run_id"]
            assert cache.dbsize() == 0, "业务测试专用 Redis DB 必须为空"
            cache_owned = True
            cursor.execute(
                f"CREATE DATABASE `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            database_created = True
            cursor.execute(f"USE `{name}`")
            for module in ("system", "infra") if part == "infra" else ("system",):
                for sql in sorted((root / "dushan-admin-backend/sql/mysql" / module).glob("*.sql")):
                    cursor.execute(sql.read_text(encoding="utf-8"))
                    while cursor.nextset():
                        pass
            password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
            cursor.execute(
                "UPDATE system_users SET password=%s,status=1 WHERE username='admin'", (password,)
            )
            cursor.execute(
                "UPDATE system_oauth2_client SET secret=%s WHERE client_id='default'",
                ("dushan-admin-secret",),
            )
        yield resources, name, connection
    finally:
        if database_created:
            with connection.cursor() as cursor:
                cursor.execute(f"DROP DATABASE `{name}`")
        connection.close()
        # DB 10/11 在资源清单中专供本测试拥有；只删除本次空库启动后产生的键。
        if cache_owned:
            keys = list(cache.scan_iter())
            if keys:
                cache.delete(*keys)
        cache.close()
