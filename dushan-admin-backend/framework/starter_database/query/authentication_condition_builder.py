from sqlalchemy import false, true

from framework.starter_database.query.row_statement_filter import RowStatementFilter


class AuthenticationConditionBuilder(RowStatementFilter):
    """认证查询限定服务端登记的模型，并隐藏软删除记录。"""

    def __init__(self, registry):
        super().__init__(registry, lambda: ValueError("认证读取声明无效"))

    def condition(self, config, operation, *, orm=False, entity=None):
        if "deleted" in config.table.c:
            return self._column(config, "deleted", orm, entity) == false()
        return true()
