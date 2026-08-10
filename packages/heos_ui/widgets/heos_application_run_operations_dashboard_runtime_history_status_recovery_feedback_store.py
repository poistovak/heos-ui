from __future__ import annotations

import importlib
from dataclasses import dataclass, field

feedback_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_feedback"
)

RecoveryFeedback = (
    feedback_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedback
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackStore:
    _entries: list[RecoveryFeedback] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self._entries)

    @property
    def empty(self) -> bool:
        return not self._entries

    @property
    def latest(self) -> RecoveryFeedback | None:
        if not self._entries:
            return None
        return self._entries[-1]

    @property
    def history(self) -> tuple[RecoveryFeedback, ...]:
        return tuple(self._entries)

    @property
    def learned_only(self) -> tuple[RecoveryFeedback, ...]:
        return tuple(
            entry
            for entry in self._entries
            if entry.learned
        )

    def append(
        self,
        feedback: RecoveryFeedback,
    ) -> None:
        self._entries.append(feedback)

    def by_code(
        self,
        diagnostic_code: str,
    ) -> tuple[RecoveryFeedback, ...]:
        return tuple(
            entry
            for entry in self._entries
            if entry.diagnostic_code == diagnostic_code
        )

    def clear(self) -> None:
        self._entries.clear()
