from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_runtime import (
    HEOSApplicationRunOperationsDashboardRuntime,
    HEOSApplicationRunOperationsDashboardRuntimeCycle,
)
from .heos_application_run_operations_dashboard_runtime_history import (
    HEOSApplicationRunOperationsDashboardRuntimeHistory,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryController:
    runtime: HEOSApplicationRunOperationsDashboardRuntime
    history: HEOSApplicationRunOperationsDashboardRuntimeHistory

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryController:
        return cls(
            runtime=HEOSApplicationRunOperationsDashboardRuntime.create(),
            history=HEOSApplicationRunOperationsDashboardRuntimeHistory(),
        )

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle | None:
        return self.history.latest

    @property
    def cycle_count(self) -> int:
        return self.history.count

    @property
    def has_cycles(self) -> bool:
        return not self.history.empty

    def run(
        self,
        operations: HEOSApplicationRunOperationsSession,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle:
        cycle = self.runtime.run(operations)
        self.history.append(cycle)

        return cycle

    def get(
        self,
        cycle_number: int,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle | None:
        return self.history.get(cycle_number)

    def clear(self) -> None:
        self.runtime.clear()
        self.history.clear()
