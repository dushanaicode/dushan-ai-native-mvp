from sqlalchemy import (
    BigInteger,
    Computed,
    ForeignKeyConstraint,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from framework.starter_data_permission.public import (
    data_permission,
)
from framework.starter_database.public import BaseDO


@data_permission(
    permission_type="user_scope", user_id_column="user_id", description="用户岗位表-用户权限"
)
class UserPostDO(BaseDO):
    __tablename__ = "system_user_post"
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", "active_key", name="uq_system_user_post_active_0"),
        ForeignKeyConstraint(["user_id"], ["system_users.id"], name="fk_system_user_post_user_id"),
        ForeignKeyConstraint(["post_id"], ["system_post.id"], name="fk_system_user_post_post_id"),
        {**BaseDO.__table_args__, **{"comment": "用户岗位表"}},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="用户ID")
    post_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="岗位ID")

    active_key: Mapped[int | None] = mapped_column(
        SmallInteger,
        Computed("CASE WHEN deleted = 0 THEN 1 ELSE NULL END"),
        comment="仅有效记录参与业务唯一约束",
    )
