from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class JobSignalDO(BaseDO):
    __tablename__ = "infra_job_signal"
    __table_args__ = {**BaseDO.__table_args__, "comment": "调度器持久协调记录"}

    revision: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, comment="任务定义提交后的合并通知版本"
    )
