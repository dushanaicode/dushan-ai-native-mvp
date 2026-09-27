from contextlib import asynccontextmanager

from fastapi import Request

from framework.starter_di.public import Inject, service
from framework.starter_security.public import (
    PublicRequestContextProvider,
    SecurityErrorCodes,
    SecurityException,
)
from module_system.config.system_settings import SystemSettings
from module_system.controller.admin.auth.auth_cookies import AuthCookies
from module_system.definitions.constants.public_contexts import PublicContexts
from module_system.framework.sms.sms_callback_token import SmsCallbackToken
from module_system.service.workload.system_workload_service import SystemWorkloadService


@service(interface=PublicRequestContextProvider)
class SystemPublicRequestContextProvider(PublicRequestContextProvider):
    settings: SystemSettings = Inject()
    workloads: SystemWorkloadService = Inject()

    def validate(self, name: str) -> None:
        if name not in PublicContexts.NAMES:
            raise ValueError(f"未登记的公开上下文：{name}")

    def parameters(self, name: str) -> tuple[dict, ...]:
        self.validate(name)
        if name == PublicContexts.AUTHENTICATION:
            return ()
        if name == PublicContexts.SMS_CALLBACK:
            return (
                {
                    "in": "query",
                    "name": "token",
                    "required": True,
                    "schema": {"type": "string", "maxLength": 129},
                },
            )
        return (
            {
                "in": "cookie",
                "name": "system_social_binding",
                "required": True,
                "schema": {"type": "string"},
            },
        )

    @asynccontextmanager
    async def enter(self, request: Request, name: str):
        self.validate(name)
        channel_id = None
        if name == PublicContexts.SMS_CALLBACK:
            tokens = request.query_params.getlist("token")
            if len(tokens) != 1 or set(request.query_params) != {"token"}:
                raise SecurityException(SecurityErrorCodes.INVALID)
            channel_id = SmsCallbackToken.verify(self.settings.sms_callback_token, tokens[0])
            capability = "system.sms.send"
        else:
            AuthCookies.check_origin(request, self.settings)
            if name == PublicContexts.SOCIAL_LOGIN:
                binding = request.cookies.get("system_social_binding")
                if binding is None or not 32 <= len(binding) <= 1024:
                    raise SecurityException(SecurityErrorCodes.INVALID)
                # 一次性 state 和浏览器绑定由 AuthService.complete 验证。
            capability = "system.auth"
        async with self.workloads.scope(capability):
            if channel_id is not None:
                request.state.sms_callback_channel_id = channel_id
            try:
                yield
            finally:
                if channel_id is not None:
                    request.scope["state"].pop("sms_callback_channel_id")
