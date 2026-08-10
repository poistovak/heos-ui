from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

experience_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_experience"
)

RecoveryExperience = (
    experience_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExperience
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState(
    str,
    Enum,
):
    COLD_START = "cold_start"
    RETRY_SUPPORTED = "retry_supported"
    RETRY_DISCOURAGED = "retry_discouraged"
    MANUAL_REQUIRED = "manual_required"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicy:
    diagnostic_code: str
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState
    )
    allow_retry: bool
    confidence: float
    reason: str

    @classmethod
    def evaluate(
        cls,
        experience: RecoveryExperience,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicy:
        if experience.empty:
            return cls(
                diagnostic_code=experience.diagnostic_code,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState.COLD_START
                ),
                allow_retry=True,
                confidence=0.0,
                reason="No recovery experience is available yet.",
            )

        if experience.manual > 0:
            return cls(
                diagnostic_code=experience.diagnostic_code,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState.MANUAL_REQUIRED
                ),
                allow_retry=False,
                confidence=1.0,
                reason="Historical recovery includes manual intervention.",
            )

        if experience.retry_supported:
            return cls(
                diagnostic_code=experience.diagnostic_code,
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState.RETRY_SUPPORTED
                ),
                allow_retry=True,
                confidence=(
                    experience.success_rate
                    if experience.success_rate is not None
                    else 0.0
                ),
                reason="Historical recovery supports another retry.",
            )

        return cls(
            diagnostic_code=experience.diagnostic_code,
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState.RETRY_DISCOURAGED
            ),
            allow_retry=False,
            confidence=(
                1.0 - experience.success_rate
                if experience.success_rate is not None
                else 0.0
            ),
            reason="Historical recovery does not support another retry.",
        )
