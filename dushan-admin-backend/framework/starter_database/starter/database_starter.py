from loguru import logger

from framework.starter_database.session.session_provider import SessionProvider
from framework.starter_di.context.application_context import ApplicationContext
from framework.starter_di.context.application_state_enum import ApplicationStateEnum
from framework.starter_di.context.di_task_runner import DiTaskRunner
from framework.starter_di.decorators.components import starter


@starter
class DatabaseStarter:
    """将单库资源接入应用任务与关闭协调，连接配置只在启动期加载。"""

    def __init__(
        self, database: SessionProvider, tasks: DiTaskRunner, application: ApplicationContext
    ):
        self.database, self.application = database, application
        self.database.bind_task_runner(tasks)

    async def open(self) -> None:
        await self.database.open()
        logger.info(
            "【DatabaseStarter】主库就绪：ID 策略={}，健康检查={}",
            self.database.settings.id_strategy,
            self.database.settings.health_check_enabled,
        )

    async def close(self) -> None:
        if self.application.state is ApplicationStateEnum.STARTING:
            self.database._transactions.cancel_callbacks()
        await self.database.close()
