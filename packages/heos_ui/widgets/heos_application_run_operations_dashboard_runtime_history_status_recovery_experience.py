from __future__ import annotations

import importlib
from dataclasses import dataclass

feedback_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_feedback"
)
store_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_feedback_store"
)

FeedbackState = (
    feedback_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackState
)
FeedbackStore = (
    store_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryFeedbackStore
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExperience:
    diagnostic_code: str
    observations: int
    positive: int
    negative: int
    manual: int
    success_rate: float | None
    retry_supported: bool

    @property
    def empty(self) -> bool:
        return self.observations == 0

    @classmethod
    def from_store(
        cls,
        store: FeedbackStore,
        diagnostic_code: str,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExperience:
        entries = tuple(
            entry
            for entry in store.by_code(diagnostic_code)
            if entry.learned
        )

        positive = sum(
            entry.state is FeedbackState.POSITIVE
            for entry in entries
        )
        negative = sum(
            entry.state is FeedbackState.NEGATIVE
            for entry in entries
        )
        manual = sum(
            entry.state is FeedbackState.MANUAL
            for entry in entries
        )

        observations = len(entries)
        completed = positive + negative

        success_rate = (
            positive / completed
            if completed
            else None
        )

        retry_supported = (
            negative > 0
            and manual == 0
            and any(
                entry.retry_recommended
                for entry in entries
            )
        )

        return cls(
            diagnostic_code=diagnostic_code,
            observations=observations,
            positive=positive,
            negative=negative,
            manual=manual,
            success_rate=success_rate,
            retry_supported=retry_supported,
        )
