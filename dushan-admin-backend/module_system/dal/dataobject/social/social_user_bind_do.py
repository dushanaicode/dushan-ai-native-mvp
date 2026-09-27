from sqlalchemy import (
    BigInteger,
    Computed,
    ForeignKeyConstraint,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class SocialUserBindDO(BaseDO):
    __tablename__ = "system_social_user_bind"
    __table_args__ = (
        UniqueConstraint(
            "user_type",
            "social_type",
            "social_user_id",
            "active_key",
            name="uq_system_social_user_bind_active_0",
        ),
        UniqueConstraint(
            "user_type",
            "social_type",
            "user_id",
            "active_key",
            name="uq_system_social_user_bind_active_1",
        ),
        ForeignKeyConstraint(
            ["social_user_id"],
            ["system_social_user.id"],
            name="fk_system_social_user_bind_social_user_id",
        ),
        {**BaseDO.__table_args__, **{"comment": "社交绑定表"}},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户编号")
    user_type: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, comment="用户类型（枚举）【UserTypeEnum】"
    )
    social_type: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, comment="社交平台的类型【SocialTypeEnum】"
    )
    social_user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="社交用户的编号"
    )

    active_key: Mapped[int | None] = mapped_column(
        SmallInteger,
        Computed("CASE WHEN deleted = 0 THEN 1 ELSE NULL END"),
        comment="仅有效记录参与业务唯一约束",
    )
