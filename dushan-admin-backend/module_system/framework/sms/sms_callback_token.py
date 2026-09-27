import base64
import binascii
import hashlib
import hmac
import re

from pydantic import SecretStr

from framework.common.contracts import SnowflakeId
from framework.starter_security.public import SecurityErrorCodes, SecurityException


class SmsCallbackToken:
    @staticmethod
    def _key(secret: SecretStr | None) -> bytes:
        if secret is None or len(secret.get_secret_value()) < 32:
            raise SecurityException(SecurityErrorCodes.CONFIGURATION)
        return secret.get_secret_value().encode()

    @classmethod
    def create(cls, secret: SecretStr | None, channel_id: int) -> str:
        """签名凭据绑定服务器确定的渠道，回执不能改选其他渠道。"""
        payload = base64.urlsafe_b64encode(str(channel_id).encode()).decode().rstrip("=")
        signature = hmac.new(
            cls._key(secret), ("sms-callback:" + payload).encode(), hashlib.sha256
        ).hexdigest()
        return payload + "." + signature

    @classmethod
    def verify(cls, secret: SecretStr | None, token: str) -> int:
        key = cls._key(secret)
        if re.fullmatch(r"[A-Za-z0-9_-]{2,26}\.[0-9a-f]{64}", token) is None:
            raise SecurityException(SecurityErrorCodes.INVALID)
        payload, signature = token.split(".")
        expected = hmac.new(key, ("sms-callback:" + payload).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise SecurityException(SecurityErrorCodes.INVALID)
        try:
            channel_id = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)).decode(
                "ascii"
            )
            return int(SnowflakeId.format(channel_id))
        except (binascii.Error, UnicodeDecodeError, ValueError) as error:
            raise SecurityException(SecurityErrorCodes.INVALID) from error
