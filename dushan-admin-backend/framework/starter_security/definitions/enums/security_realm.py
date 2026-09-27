from framework.common.enums.base_enum import BaseEnum


class SecurityRealm(BaseEnum):
    """本站账号身份域；公开是路由属性，服务执行由独立 WorkloadIdentity 表达。"""

    ACCOUNT = ("account", "本站账号")
    CLIENT = ("client", "本站应用客户端")
