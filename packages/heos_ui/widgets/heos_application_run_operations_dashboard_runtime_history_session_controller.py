from __future__ import annotations

from dataclasses import dataclass

from . import (
    heos_application_run_operations_dashboard_runtime_history_session as history_session,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

HistorySession = (
    history_session.HEOSApplicationRunOperationsDashboardRuntimeHistorySession
)
HistoryUpdate = (
    history_session.HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistorySessionController:
    session: HistorySession
    _running: bool = False
    _tick_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySessionController:
        return cls(
            session=HistorySession.create(),
        )

    @property
    def running(self) -> bool:
        return self._running

    @property
    def tick_count(self) -> int:
        return self._tick_count

    @property
    def latest(self) -> HistoryUpdate | None:
        return self.session.latest

    @property
    def has_updates(self) -> bool:
        return self.session.has_updates

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def tick(
        self,
        operations: HEOSApplicationRunOperationsSession,
    ) -> HistoryUpdate:
        if not self._running:
            raise RuntimeError(
                "Runtime history session controller is not running."
            )

        update = self.session.refresh(operations)
        self._tick_count += 1
        return update

    def reset(self) -> None:
        self.session.clear()
        self._running = False
        self._tick_count = 0
