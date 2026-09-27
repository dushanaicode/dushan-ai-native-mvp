from framework.starter_data_permission.core.condition_builder import ConditionBuilder
from framework.starter_data_permission.definitions.constants.data_permission_error_codes import (
    DataPermissionErrorCodes,
)
from framework.starter_data_permission.exception.data_permission_exception import (
    DataPermissionException,
)
from framework.starter_database.definitions.constants.row_access_error_codes import (
    RowAccessErrorCodes,
)
from framework.starter_database.query.row_access_rule import RowAccessRule


class DataPermissionPolicy(RowAccessRule):
    """数据范围规则；统一 SQL 改写和完整写入预检查。"""

    def __init__(self, registry, service):
        self.registry, self.service = registry, service
        self.builder = ConditionBuilder(registry, service)

    def scope_key(self):
        return self.service.execution_key()

    def condition(self, config, operation, *, orm=False, entity=None):
        return self.builder.condition(config, operation, orm=orm, entity=entity)

    def failure(self, reason):
        return DataPermissionException(
            {
                RowAccessErrorCodes.STALE: DataPermissionErrorCodes.STALE,
                RowAccessErrorCodes.CONFIGURATION: DataPermissionErrorCodes.CONFIGURATION,
                RowAccessErrorCodes.WRITE: DataPermissionErrorCodes.WRITE,
            }[reason]
        )

    def validate_row(self, config, row, operation):
        if config.public:
            return
        frame = self.service.current()
        for name in config.authority_columns:
            if name not in row or (
                row[name] is not None
                and type(row[name]) is not config.table.c[name].type.python_type
            ):
                raise DataPermissionException(DataPermissionErrorCodes.WRITE)
        if self.service.is_exempt(config.resource, operation) or frame.grant.all_data:
            return
        if not (
            config.user_column is not None
            and row[config.user_column]
            in config.scope_values(config.user_column, frame.grant.user_ids)
            or config.department_column is not None
            and row[config.department_column]
            in config.scope_values(config.department_column, frame.grant.department_ids)
        ):
            raise DataPermissionException(DataPermissionErrorCodes.WRITE)
