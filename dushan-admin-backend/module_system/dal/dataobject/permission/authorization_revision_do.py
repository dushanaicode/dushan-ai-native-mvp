from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class AuthorizationRevisionDO(BaseDO):
    """权限元数据版本，与权限变更在同一事务提交；初始 SQL 创建 id=1。"""

    __tablename__ = "system_authorization_revision"
    __table_args__ = {**BaseDO.__table_args__, "comment": "系统授权版本"}
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False, default=1)
