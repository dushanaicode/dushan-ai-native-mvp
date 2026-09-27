from sqlalchemy import Computed, Integer, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from framework.common.enums import StatusEnum
from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class PostDO(BaseDO):
    __tablename__ = "system_post"
    __table_args__ = (
        UniqueConstraint("code", "active_key", name="uq_system_post_active_0"),
        {**BaseDO.__table_args__, **{"comment": "岗位信息表"}},
    )

    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位编码")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="岗位名称")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="显示顺序")
    status: Mapped[int] = mapped_column(
        SmallInteger,
        default=StatusEnum.ENABLE.code,
        comment="开启状态（1-启用，0-禁用）【StatusEnum】",
    )
    remark: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="备注")

    active_key: Mapped[int | None] = mapped_column(
        SmallInteger,
        Computed("CASE WHEN deleted = 0 THEN 1 ELSE NULL END"),
        comment="仅有效记录参与业务唯一约束",
    )
