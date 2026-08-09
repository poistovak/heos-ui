from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsSessionStatistics:
    total_updates: int
    idle_updates: int
    healthy_updates: int
    degraded_updates: int
    rendered_frames: int
    latest_sequence: int | None

    @property
    def active_updates(self) -> int:
        return self.healthy_updates + self.degraded_updates

    @property
    def empty(self) -> bool:
        return self.total_updates == 0

    @property
    def healthy(self) -> bool:
        return (
            self.total_updates > 0
            and self.degraded_updates == 0
        )

    @classmethod
    def capture(
        cls,
        session: HEOSApplicationRunOperationsSession,
    ) -> HEOSApplicationRunOperationsSessionStatistics:
        history = session.history

        idle_updates = 0
        healthy_updates = 0
        degraded_updates = 0
        rendered_frames = 0

        for update in history:
            status = update.view.status

            if status == "IDLE":
                idle_updates += 1
            elif status == "HEALTHY":
                healthy_updates += 1
            elif status == "DEGRADED":
                degraded_updates += 1

            if update.frame.command_count > 0:
                rendered_frames += 1

        latest_sequence = (
            history[-1].sequence
            if history
            else None
        )

        return cls(
            total_updates=len(history),
            idle_updates=idle_updates,
            healthy_updates=healthy_updates,
            degraded_updates=degraded_updates,
            rendered_frames=rendered_frames,
            latest_sequence=latest_sequence,
        )
