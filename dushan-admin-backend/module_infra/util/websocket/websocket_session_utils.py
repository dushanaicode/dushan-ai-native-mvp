from framework.starter_di.public import (
    util,
)
from framework.starter_websocket.public import (
    SocketTarget,
    SocketTargetKind,
)


@util
class WebSocketSessionUtils:
    def target(self, member_id=None, client_id=None):
        return SocketTarget(
            kind=SocketTargetKind.CLIENT
            if client_id
            else SocketTargetKind.MEMBER
            if member_id
            else SocketTargetKind.AUDIENCE,
            audience="infra",
            member_id=member_id,
            client_id=client_id,
        )
