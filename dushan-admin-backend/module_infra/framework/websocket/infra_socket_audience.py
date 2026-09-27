from framework.starter_security.public import (
    SecurityRealm,
)
from framework.starter_web.public import (
    RoutePolicy,
)
from framework.starter_websocket.public import (
    AudienceDefinition,
    socket_audience,
)


@socket_audience(
    AudienceDefinition(
        key="infra",
        policy=RoutePolicy(realm=SecurityRealm.ACCOUNT),
        send_policy=RoutePolicy(permissions=("infra:websocket:send",), realm=SecurityRealm.ACCOUNT),
        workload_capability=None,
        allow_global_targets=False,
    )
)
class InfraSocketAudience:
    pass
