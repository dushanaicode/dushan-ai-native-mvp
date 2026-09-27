from framework.starter_di.public import (
    Inject,
)
from framework.starter_mq.public import (
    ConsumerDefinition,
    ExhaustedPolicy,
    MessageHandler,
    MessageMode,
    RetryPolicy,
    consumer,
)
from framework.starter_security.public import SecurityRealm
from framework.starter_web.public import (
    RoutePolicy,
)
from module_system.mq.message.sms.sms_send_message import SmsSendMessage
from module_system.service.sms.sms_send_service import SmsSendService


@consumer(
    ConsumerDefinition(
        key="system.sms.send",
        destination="sms:send",
        mode=MessageMode.STREAM,
        message=SmsSendMessage,
        group="sms-consumers",
        retry=RetryPolicy(count=3, delay_seconds=1, backoff=2, max_delay_seconds=30),
        exhausted=ExhaustedPolicy.DEAD_LETTER,
        session_policy=RoutePolicy(realm=SecurityRealm.ACCOUNT),
        workload_capabilities=frozenset({"system.sms.send"}),
    )
)
class SmsSendConsumer(MessageHandler):
    sms_send_service: SmsSendService = Inject()

    async def handle(self, message: SmsSendMessage, context) -> None:
        await self.sms_send_service.do_send_sms(message)
