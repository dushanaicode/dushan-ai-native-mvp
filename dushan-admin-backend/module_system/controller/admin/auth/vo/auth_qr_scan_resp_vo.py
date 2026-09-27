from framework.common.schemas import BaseVO
from module_system.definitions.enums.auth.qr_login_status import QrLoginStatus


class AuthQrScanRespVO(BaseVO):
    status: QrLoginStatus
    code: str
    browser: str
    ip: str
    expires_at: int
