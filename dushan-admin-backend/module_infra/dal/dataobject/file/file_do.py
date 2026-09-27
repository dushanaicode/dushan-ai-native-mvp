from typing import Any

from sqlalchemy import JSON, BigInteger, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class FileDO(BaseDO):
    __tablename__ = "infra_file"
    __table_args__ = (
        ForeignKeyConstraint(
            ["config_id"], ["infra_file_config.id"], name="fk_infra_file_config_id"
        ),
        {**BaseDO.__table_args__, **{"comment": "文件表"}},
    )

    config_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="配置编号")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="原文件名")
    original_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="原始文件名")
    path: Mapped[str] = mapped_column(String(255), nullable=False, comment="路径，即文件名")
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False, comment="实际存储路径")
    url: Mapped[str] = mapped_column(String(255), nullable=False, comment="访问地址")
    type: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件的 MIME 类型")
    size: Mapped[int] = mapped_column(Integer, nullable=False, comment="文件大小")
    hash: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="文件哈希值")
    file_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True, comment="文件元数据"
    )
