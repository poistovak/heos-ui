from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_session import (
    HEOSApplicationRunOperationsDashboardSession,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardStatistics:
    total_refreshes: int
    idle_refreshes: int
    healthy_refreshes: int
    degraded_refreshes: int
    rendered_frames: int
    latest_sequence: int | None

    @property
    def active_refreshes(self) -> int:
        return self.healthy_refreshes + self.degraded_refreshes

    @property
    def empty(self) -> bool:
        return self.total_refreshes == 0

    @property
    def healthy(self) -> bool:
        return (
            self.total_refreshes > 0
            and self.degraded_refreshes == 0
        )

    @classmethod
    def capture(
        cls,
        session: HEOSApplicationRunOperationsDashboardSession,
    ) -> HEOSApplicationRunOperationsDashboardStatistics:
        history = session.history

        idle_refreshes = 0
        healthy_refreshes = 0
        degraded_refreshes = 0
        rendered_frames = 0

        for update in history:
            status = update.view.status

            if status == "IDLE":
                idle_refreshes += 1
            elif status == "HEALTHY":
                healthy_refreshes += 1
            elif status == "DEGRADED":
                degraded_refreshes += 1

            if update.frame.command_count > 0:
                rendered_frames += 1

        latest_sequence = (
            history[-1].sequence
            if history
            else None
        )

        return cls(
            total_refreshes=len(history),
            idle_refreshes=idle_refreshes,
            healthy_refreshes=healthy_refreshes,
            degraded_refreshes=degraded_refreshes,
            rendered_frames=rendered_frames,
            latest_sequence=latest_sequence,
        )
