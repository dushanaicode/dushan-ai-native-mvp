import hashlib
import json

from framework.starter_security.model.login_session import LoginSession


class IdentityBinding:
    """身份绑定键的唯一计算契约；字段与顺序共同决定权限缓存隔离。"""

    @staticmethod
    def build(session: LoginSession) -> str:
        values = [
            session.application_id,
            session.domain,
            session.account_id,
            session.session_id,
            session.family_id,
            session.realm.value,
        ]
        return hashlib.sha256(json.dumps(values, separators=(",", ":")).encode()).hexdigest()
