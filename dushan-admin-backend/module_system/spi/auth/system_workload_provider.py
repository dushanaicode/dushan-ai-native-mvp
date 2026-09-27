from framework.starter_di.public import (
    Inject,
    service,
)
from framework.starter_security.public import (
    WorkloadProvider,
)
from module_system.service.workload.system_workload_service import SystemWorkloadService


@service(interface=WorkloadProvider)
class SystemWorkloadProvider(WorkloadProvider):
    delegate: SystemWorkloadService = Inject()

    async def authenticate(
        self,
        source: str,
        *,
        application_id: str,
        domain: str,
        capability: str,
    ):
        return await self.delegate.authenticate(
            source,
            application_id=application_id,
            domain=domain,
            capability=capability,
        )
