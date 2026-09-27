from contextlib import AbstractAsyncContextManager
from typing import Protocol, runtime_checkable

from framework.starter_security.public import (
    WorkloadIdentity,
)


@runtime_checkable
class SystemWorkloadService(Protocol):
    async def authenticate(
        self, source: str, *, application_id: str, domain: str, capability: str
    ) -> WorkloadIdentity: ...
    def scope(self, capability: str) -> AbstractAsyncContextManager[None]: ...
