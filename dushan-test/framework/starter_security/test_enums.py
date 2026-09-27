import json

import pytest
from pydantic import ValidationError

from framework.starter_security.definitions.enums.security_realm import SecurityRealm
from framework.starter_security.model.login_session import LoginSession
from framework.starter_web.routing.route_policy import RoutePolicy


@pytest.fixture
def session_payload():
    return {
        "application_id": "enum-test",
        "domain": "admin",
        "token_digest": "a" * 64,
        "session_id": "session",
        "family_id": "family",
        "account_id": "account",
        "realm": "account",
        "expires_at": "2099-01-01T00:00:00Z",
        "revoked": False,
        "account_enabled": True,
        "credential_revision": 1,
        "current_credential_revision": 1,
        "authorization_revision": "1",
        "scopes": [],
    }


@pytest.mark.parametrize("authority", [{"realm": "account"}, {"realm": "client"}])
def test_session_enum_roundtrip_preserves_wire_codes(session_payload, authority):
    session = LoginSession.model_validate_json(json.dumps(session_payload | authority))
    assert session.realm is SecurityRealm.from_code(authority["realm"])
    assert session.realm.code == session.realm.value == authority["realm"]
    assert session.realm.label != session.realm.code
    encoded = json.loads(session.model_dump_json())
    assert all(encoded[name] == value for name, value in authority.items())
    assert LoginSession.model_validate_json(session.model_dump_json()) == session

    # JSON 边界解析编码；内部 Python 模型继续要求已经解析的枚举成员。
    with pytest.raises(ValidationError, match="realm"):
        LoginSession.model_validate(session.model_dump() | {"realm": authority["realm"]})


def test_enum_openapi_names_and_values_remain_stable():
    definitions = LoginSession.model_json_schema()["$defs"]
    assert definitions["SecurityRealm"]["type"] == "string"
    assert definitions["SecurityRealm"]["enum"] == ["account", "client"]


def test_route_policy_requires_typed_security_enums():
    with pytest.raises(TypeError, match="realm"):
        RoutePolicy(realm="account")
    assert RoutePolicy(realm=SecurityRealm.ACCOUNT).realm is SecurityRealm.ACCOUNT
