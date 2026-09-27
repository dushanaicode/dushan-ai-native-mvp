from framework.common.schemas import BaseVO


class AuthQrCreateRespVO(BaseVO):
    ticket: str
    code: str
    expires_at: int
    poll_interval: int
