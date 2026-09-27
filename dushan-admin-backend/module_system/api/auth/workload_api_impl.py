from framework.starter_di.public import (
    Inject,
    service,
)
from module_system.api.auth.workload_api import WorkloadApi
from module_system.service.workload.system_workload_service import SystemWorkloadService


@service(interface=WorkloadApi)
class WorkloadApiImpl(WorkloadApi):
    workloads: SystemWorkloadService = Inject()

    def scope(self, capability):
        return self.workloads.scope(capability)
