from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from framework.starter_security.definitions.enums.security_realm import SecurityRealm

type IdentityId = Annotated[str, Field(strict=True, min_length=1, max_length=256)]


class LoginSession(BaseModel):
    """业务提供者读取当前权威数据构建的本站会话；凭据与授权版本必须实时校验。"""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True, hide_input_in_errors=True)

    application_id: IdentityId
    domain: IdentityId
    token_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    session_id: IdentityId
    family_id: IdentityId
    account_id: Annotated[str, Field(strict=True, min_length=1, max_length=64)]
    realm: SecurityRealm
    expires_at: AwareDatetime
    revoked: bool
    account_enabled: bool
    credential_revision: int = Field(ge=1)
    current_credential_revision: int = Field(ge=1)
    authorization_revision: IdentityId
    scopes: frozenset[str]
    dept_id: IdentityId | None = None

    def __repr_args__(self):
        return iter(())
