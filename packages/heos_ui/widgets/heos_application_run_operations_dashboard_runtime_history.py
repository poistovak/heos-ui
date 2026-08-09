from __future__ import annotations

from dataclasses import dataclass, field

from .heos_application_run_operations_dashboard_runtime import (
    HEOSApplicationRunOperationsDashboardRuntimeCycle,
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistory:
    _cycles: list[
        HEOSApplicationRunOperationsDashboardRuntimeCycle
    ] = field(default_factory=list)

    @property
    def cycles(
        self,
    ) -> tuple[
        HEOSApplicationRunOperationsDashboardRuntimeCycle,
        ...,
    ]:
        return tuple(self._cycles)

    @property
    def count(self) -> int:
        return len(self._cycles)

    @property
    def empty(self) -> bool:
        return not self._cycles

    @property
    def first(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle | None:
        if not self._cycles:
            return None

        return self._cycles[0]

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle | None:
        if not self._cycles:
            return None

        return self._cycles[-1]

    def append(
        self,
        cycle: HEOSApplicationRunOperationsDashboardRuntimeCycle,
    ) -> None:
        self._cycles.append(cycle)

    def get(
        self,
        cycle_number: int,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle | None:
        for cycle in self._cycles:
            if cycle.cycle == cycle_number:
                return cycle

        return None

    def clear(self) -> None:
        self._cycles.clear()
