from typing import Literal

from pydantic import Field, model_validator

from framework.starter_config.config.config_model import ConfigModel
from framework.starter_config.decorator.config_decorator import config_model
from framework.starter_config.definitions.enums.config_source_enum import ConfigSourceEnum
from framework.starter_database.config.data_source_settings import DataSourceSettings
from framework.starter_database.config.database_pool_settings import DatabasePoolSettings


@config_model(
    "database",
    env_prefix="DATABASE_",
    sources=(ConfigSourceEnum.ENVIRONMENT, ConfigSourceEnum.YAML),
)
class DatabaseSettings(ConfigModel):
    """启动期数据库契约；一个主库连接，连接配置变更需要重启应用。"""

    enabled: bool
    sources: tuple[DataSourceSettings, ...]
    pool: DatabasePoolSettings
    connect_timeout_seconds: float = Field(gt=0)
    health_check_enabled: bool
    health_check_interval_seconds: float = Field(gt=0)
    slow_query_enabled: bool
    slow_query_threshold_ms: float = Field(ge=0)
    query_observation_enabled: bool
    query_template_enabled: bool
    query_fingerprint_enabled: bool
    query_sample_rate: float = Field(ge=0, le=1)
    query_max_statement_length: int = Field(ge=64, le=1000000)
    query_max_template_length: int = Field(ge=16, le=4096)
    soft_delete_enabled: bool
    audit_enabled: bool
    id_strategy: Literal["database", "snowflake"]
    snowflake_machine_id: int | None = Field(ge=0, le=1023)
    after_commit_result_limit: int = Field(ge=1, le=10000)

    @model_validator(mode="after")
    def validate_sources(self) -> "DatabaseSettings":
        if self.enabled and len(self.sources) != 1:
            raise ValueError("MVP 数据库必须配置一个主库连接")
        if len(self.sources) > 1:
            raise ValueError("MVP 不支持动态多源或副本路由")
        if self.enabled and self.id_strategy == "snowflake" and self.snowflake_machine_id is None:
            raise ValueError("雪花 ID 必须显式分配 snowflake_machine_id")
        return self
