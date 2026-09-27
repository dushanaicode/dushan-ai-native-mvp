from __future__ import annotations

from sqlalchemy import update

from framework.starter_database.public import (
    SessionProvider,
)
from framework.starter_di.public import (
    Inject,
    service,
)
from module_system.dal.dataobject.permission.authorization_revision_do import (
    AuthorizationRevisionDO,
)
from module_system.service.permission.authorization_revision_service import (
    AuthorizationRevisionService,
)


@service(interface=AuthorizationRevisionService)
class AuthorizationRevisionServiceImpl(AuthorizationRevisionService):
    database: SessionProvider = Inject()

    async def advance(self):
        # 全局权限元数据与本次授权修改原子提交，旧版本缓存不可继续复用。
        async with self.database.transaction() as session:
            result = await session.execute(
                update(AuthorizationRevisionDO)
                .where(AuthorizationRevisionDO.id == 1)
                .values(revision=AuthorizationRevisionDO.revision + 1)
            )
            if result.rowcount != 1:
                raise ValueError("缺少系统授权版本初始行")
