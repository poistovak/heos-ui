from __future__ import annotations

from dataclasses import dataclass, field

from .heos_application_run_live_session import (
    HEOSApplicationRunLiveSession,
)
from .heos_application_run_session_operations_controller import (
    HEOSApplicationRunSessionOperationsController,
    HEOSApplicationRunSessionOperationsUpdate,
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsSession:
    controller: HEOSApplicationRunSessionOperationsController
    _history: list[HEOSApplicationRunSessionOperationsUpdate] = field(
        default_factory=list,
        init=False,
    )

    @classmethod
    def create(cls) -> HEOSApplicationRunOperationsSession:
        return cls(
            controller=HEOSApplicationRunSessionOperationsController.create(),
        )

    @property
    def history(
        self,
    ) -> tuple[HEOSApplicationRunSessionOperationsUpdate, ...]:
        return tuple(self._history)

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunSessionOperationsUpdate | None:
        if not self._history:
            return None

        return self._history[-1]

    @property
    def update_count(self) -> int:
        return len(self._history)

    @property
    def has_updates(self) -> bool:
        return bool(self._history)

    def refresh(
        self,
        session: HEOSApplicationRunLiveSession,
    ) -> HEOSApplicationRunSessionOperationsUpdate:
        update = self.controller.update(session)
        self._history.append(update)

        return update

    def clear(self) -> None:
        self._history.clear()
        self.controller.clear()
