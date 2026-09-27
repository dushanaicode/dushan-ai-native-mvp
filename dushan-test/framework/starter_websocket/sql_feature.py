import importlib
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine

from fixtures.config_factory import ConfigFactory
from starter_websocket.provider_source import SOURCE


@asynccontextmanager
async def sql_feature(target, tmp_path, module_package):
    namespace = "s" + uuid4().hex[:10]
    package = "ws_records_" + namespace
    source = """
from sqlalchemy import MetaData, String, Integer
from sqlalchemy.orm import mapped_column
from framework.starter_database.model.base_do import BaseDO
from framework.starter_di.decorators.components import service
from framework.starter_data_permission.decorators.data_permission import data_permission
from framework.starter_data_permission.spi.data_permission_provider import DataPermissionProvider
from framework.starter_data_permission.model.data_scope_rule import DataScopeRule
from framework.starter_data_permission.definitions.enums.data_scope import DataScope

metadata = MetaData()
@data_permission(permission_type="user_scope", user_id_column="user_id")
class Record(BaseDO):
    __tablename__ = "__TABLE__"
    metadata = metadata
    user_id = mapped_column(String(64), nullable=False)
    name = mapped_column(String(64), nullable=False)
    value = mapped_column(Integer, nullable=False)

@service(interface=DataPermissionProvider)
class RecordRules(DataPermissionProvider):
    async def rules(self, identity): return (DataScopeRule(scope=DataScope.SELF),)
    async def descendants(self, identity, department_id): return frozenset()
    async def users(self, identity, department_ids): return frozenset()
    async def revision(self, identity): return identity.authorization_revision
""".replace("__TABLE__", package)
    module_package(package, scan_roots=(".",), files={"components.py": source})
    module = importlib.import_module(package + ".components")
    uri = target["url"] or f"sqlite+aiosqlite:///{(tmp_path / 'websocket.sqlite').as_posix()}"
    database = {
        **ConfigFactory.values()["config"]["models"]["database"],
        "enabled": True,
        "health_check_enabled": False,
        "sources": [dict(name="primary", url=uri, role="primary", pool=None, tls=None)],
    }
    engine = create_async_engine(uri)
    try:
        async with engine.begin() as connection:
            await connection.run_sync(module.metadata.create_all)
            now = datetime.now(UTC).replace(tzinfo=None)
            audit = dict(create_time=now, update_time=now)
            await connection.execute(
                insert(module.Record.__table__),
                [
                    dict(
                        id=index,
                        user_id=member,
                        name=name,
                        value=index,
                        **audit,
                    )
                    for index, member, name in (
                        (1, "m1", "first-member"),
                        (2, "m2", "second-member"),
                        (3, "m3", "third-member"),
                    )
                ],
            )
        websocket_source = SOURCE
        websocket_source += f"""
from {package}.components import Record
from sqlalchemy import select
from framework.starter_database.session.session_provider import SessionProvider
from framework.starter_websocket.spi.socket_projection import SocketProjection

class RecordsPayload(BaseModel):
    ids: list[int]
    names: list[str]=[]

@service
class RecordsProjection(SocketProjection):
    def __init__(self,database: SessionProvider): self.database=database
    async def project(self,payload,context):
        async with self.database.read_session() as session:
            names=list((await session.scalars(select(Record.__table__.c.name).where(Record.id.in_(payload.ids),Record.value>0))).all())
        return RecordsPayload(ids=payload.ids,names=names)

@socket_event(EventDefinition(audience="test",type="records",payload=RecordsPayload,policy=read,projector=RecordsProjection))
class RecordsEvent:
    pass

@socket_handler(HandlerDefinition(audience="test",type="records",payload=RecordsPayload,policy=read))
class RecordsHandler(SocketHandler):
    async def handle(self,payload,context): await context.reply("records",payload)

@controller("/api/ws-sql",policy=read)
class SqlController:
    def __init__(self,database: SessionProvider,service: WebSocketService): self.database,self.service=database,service
    @route("/pool")
    async def pool(self): return self.database.get_metrics()
    @route("/send-direct",methods=("POST",))
    async def send_direct(self,command: SendInput):
        result=await self.service.send(command.target,command.message)
        return {{"accepted":result.accepted}}
"""
        yield SimpleNamespace(
            namespace=namespace,
            package=package,
            source=websocket_source,
            module=module,
            engine=engine,
            models={"database": database, "data_permission": {"enabled": True}},
        )
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(module.metadata.drop_all)
        await engine.dispose()
