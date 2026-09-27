from sqlalchemy import bindparam, false, or_, true

from framework.starter_data_permission.definitions.constants.data_permission_error_codes import (
    DataPermissionErrorCodes,
)
from framework.starter_data_permission.exception.data_permission_exception import (
    DataPermissionException,
)
from framework.starter_database.query.row_statement_filter import RowStatementFilter


class ConditionBuilder(RowStatementFilter):
    """在统一行过滤机制上计算用户、部门及显式豁免条件。"""

    def __init__(self, registry, service):
        super().__init__(
            registry, lambda: DataPermissionException(DataPermissionErrorCodes.CONFIGURATION)
        )
        self.service = service

    def condition(self, config, operation, *, orm=False, entity=None):
        if config.public:
            return true()
        frame = self.service.current()
        if self.service.is_exempt(config.resource, operation) or frame.grant.all_data:
            return true()
        conditions = []
        for name, values in (
            (config.user_column, frame.grant.user_ids),
            (config.department_column, frame.grant.department_ids),
        ):
            if name is not None and values:
                size = self.service.settings.in_clause_chunk_size
                ordered = sorted(config.scope_values(name, values))
                conditions.extend(
                    self._column(config, name, orm, entity).in_(
                        bindparam(
                            "_dushan_dp_scope",
                            ordered[start : start + size],
                            expanding=True,
                            unique=True,
                        )
                    )
                    for start in range(0, len(ordered), size)
                )
        return or_(*conditions) if conditions else false()
