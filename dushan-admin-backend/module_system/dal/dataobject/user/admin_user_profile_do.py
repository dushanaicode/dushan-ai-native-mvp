from sqlalchemy import (
    JSON,
    BigInteger,
    Computed,
    ForeignKeyConstraint,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class AdminUserProfileDO(BaseDO):
    __tablename__ = "system_user_profiles"
    __table_args__ = (
        UniqueConstraint("user_id", "active_key", name="uq_system_user_profiles_active_0"),
        ForeignKeyConstraint(
            ["user_id"], ["system_users.id"], name="fk_system_user_profiles_user_id"
        ),
        {**BaseDO.__table_args__, **{"comment": "用户详情表"}},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="个人简介")
    tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True, comment="用户标签")
    address: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="地址")
    skills: Mapped[list[str] | None] = mapped_column(JSON, nullable=True, comment="技能标签")
    work_scope: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="工作职责描述"
    )
    expertise: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="专业领域")
    communication_style: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="沟通风格（formal/casual/technical）"
    )
    ai_preference: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="AI 交互偏好（用户主动设置）"
    )

    active_key: Mapped[int | None] = mapped_column(
        SmallInteger,
        Computed("CASE WHEN deleted = 0 THEN 1 ELSE NULL END"),
        comment="仅有效记录参与业务唯一约束",
    )
