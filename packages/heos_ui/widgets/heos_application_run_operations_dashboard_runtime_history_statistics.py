from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_runtime_history import (
    HEOSApplicationRunOperationsDashboardRuntimeHistory,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics:
    total_cycles: int
    idle_cycles: int
    healthy_cycles: int
    degraded_cycles: int
    rendered_frames: int
    latest_cycle: int | None

    @property
    def active_cycles(self) -> int:
        return self.healthy_cycles + self.degraded_cycles

    @property
    def empty(self) -> bool:
        return self.total_cycles == 0

    @property
    def healthy(self) -> bool:
        return (
            self.total_cycles > 0
            and self.degraded_cycles == 0
        )

    @classmethod
    def capture(
        cls,
        history: HEOSApplicationRunOperationsDashboardRuntimeHistory,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics:
        cycles = history.cycles

        idle_cycles = 0
        healthy_cycles = 0
        degraded_cycles = 0
        rendered_frames = 0

        for cycle in cycles:
            status = cycle.view.status

            if status == "IDLE":
                idle_cycles += 1
            elif status == "HEALTHY":
                healthy_cycles += 1
            elif status == "DEGRADED":
                degraded_cycles += 1

            if cycle.frame.command_count > 0:
                rendered_frames += 1

        latest_cycle = (
            cycles[-1].cycle
            if cycles
            else None
        )

        return cls(
            total_cycles=len(cycles),
            idle_cycles=idle_cycles,
            healthy_cycles=healthy_cycles,
            degraded_cycles=degraded_cycles,
            rendered_frames=rendered_frames,
            latest_cycle=latest_cycle,
        )
