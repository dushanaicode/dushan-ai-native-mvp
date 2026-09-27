from dataclasses import dataclass
from typing import ClassVar

from framework.starter_security.definitions.enums.security_realm import SecurityRealm


@dataclass(frozen=True, slots=True)
class RoutePolicy:
    """明确公开或要求认证；可装饰原生端点/路由器，None 只代表尚未声明。"""

    ATTRIBUTE: ClassVar[str] = "__web_access_policy__"
    permissions: tuple[str, ...] = ()
    requires_identity: bool = True
    public_context: str | None = None
    roles: tuple[str, ...] = ()
    scopes: tuple[str, ...] = ()
    realm: SecurityRealm | None = None
    domain: str | None = None
    permission_mode: str = "all"
    role_mode: str = "all"
    scope_mode: str = "all"

    @staticmethod
    def resolve(
        inherited: "RoutePolicy | None", declared: "RoutePolicy | None"
    ) -> "RoutePolicy | None":
        """保护声明只能继承或一致重复；公开容器可以增加访问保护。"""
        if inherited is not None and declared is not None and inherited != declared:
            if (
                inherited.requires_identity
                or not declared.requires_identity
                or (
                    inherited.public_context is not None
                    and inherited.public_context != declared.public_context
                )
            ):
                raise ValueError("外层与内层访问声明冲突")
        return inherited if declared is None else declared

    @classmethod
    def public(cls, *, context: str | None = None) -> "RoutePolicy":
        return cls(requires_identity=False, public_context=context)

    def __call__(self, owner):
        previous = getattr(owner, self.ATTRIBUTE, None)
        if previous is not None and previous != self:
            raise ValueError("公开/保护声明冲突")
        setattr(owner, self.ATTRIBUTE, self)
        return owner

    def __post_init__(self) -> None:
        if self.public_context is not None and (
            self.requires_identity
            or not isinstance(self.public_context, str)
            or not self.public_context
            or self.public_context != self.public_context.strip()
            or len(self.public_context) > 128
        ):
            raise ValueError("公开上下文必须在公开路由声明明确的登记名称")
        if type(self.requires_identity) is not bool:
            raise TypeError("公开声明必须是布尔值")
        if not self.requires_identity and (
            self.permissions or self.roles or self.scopes or self.realm or self.domain
        ):
            raise ValueError("公开路由不能声明身份或权限")
        for values in (self.permissions, self.roles, self.scopes):
            if not isinstance(values, tuple) or any(
                not isinstance(item, str) or not item or item != item.strip() for item in values
            ):
                raise ValueError("权限声明必须是非空规范字符串元组")
            if len(values) != len(set(values)):
                raise ValueError("权限声明不能重复")
        if self.realm is not None and not isinstance(self.realm, SecurityRealm):
            raise TypeError("realm 必须使用 SecurityRealm")
        if self.domain is not None and (not self.domain or self.domain != self.domain.strip()):
            raise ValueError("认证域声明无效")
        if any(
            mode not in {"all", "any"}
            for mode in (self.permission_mode, self.role_mode, self.scope_mode)
        ):
            raise ValueError("权限、角色和 scope 组合策略必须是 all 或 any")
