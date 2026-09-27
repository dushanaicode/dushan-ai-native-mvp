from pydantic import BaseModel, ConfigDict, model_validator

from framework.starter_security.model.login_session import IdentityId


class DataGrant(BaseModel):
    """空集合明确拒绝；全量仅表示当前应用中明确授权的受控资源。"""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid", hide_input_in_errors=True)

    all_data: bool = False
    user_ids: frozenset[IdentityId] = frozenset()
    department_ids: frozenset[IdentityId] = frozenset()

    @model_validator(mode="after")
    def validate_grant(self):
        if self.all_data and (self.user_ids or self.department_ids):
            raise ValueError("全量授权不能同时包含范围集合")
        return self

    def __repr_args__(self):
        return iter(())
