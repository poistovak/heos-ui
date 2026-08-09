from __future__ import annotations

from dataclasses import dataclass, field

from .heos_application_run_operations_dashboard_controller import (
    HEOSApplicationRunOperationsDashboardController,
    HEOSApplicationRunOperationsDashboardUpdate,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardSession:
    controller: HEOSApplicationRunOperationsDashboardController
    _history: list[HEOSApplicationRunOperationsDashboardUpdate] = field(
        default_factory=list,
        init=False,
    )

    @classmethod
    def create(cls) -> HEOSApplicationRunOperationsDashboardSession:
        return cls(
            controller=HEOSApplicationRunOperationsDashboardController.create(),
        )

    @property
    def history(
        self,
    ) -> tuple[HEOSApplicationRunOperationsDashboardUpdate, ...]:
        return tuple(self._history)

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardUpdate | None:
        if not self._history:
            return None

        return self._history[-1]

    @property
    def refresh_count(self) -> int:
        return len(self._history)

    @property
    def has_updates(self) -> bool:
        return bool(self._history)

    def refresh(
        self,
        session: HEOSApplicationRunOperationsSession,
    ) -> HEOSApplicationRunOperationsDashboardUpdate:
        update = self.controller.update(session)
        self._history.append(update)

        return update

    def clear(self) -> None:
        self._history.clear()
        self.controller.clear()
