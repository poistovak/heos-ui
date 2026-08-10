from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)
policy_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "experience_policy"
)

RecoveryDecision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)
RecoveryDecisionState = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
)
ExperiencePolicy = (
    policy_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicy
)
ExperiencePolicyState = (
    policy_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState(
    str,
    Enum,
):
    ALLOW = "allow"
    BLOCK = "block"
    HOLD = "hold"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGate:
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState
    )
    diagnostic_code: str
    execute: bool
    confidence: float
    reason: str

    @classmethod
    def evaluate(
        cls,
        decision: RecoveryDecision,
        policy: ExperiencePolicy,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGate:
        if decision.diagnostic_code != policy.diagnostic_code:
            raise ValueError(
                "Recovery decision and experience policy codes do not match."
            )

        if decision.state is RecoveryDecisionState.SKIP:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState.BLOCK
                ),
                diagnostic_code=decision.diagnostic_code,
                execute=False,
                confidence=policy.confidence,
                reason="Recovery decision does not require execution.",
            )

        if decision.state is RecoveryDecisionState.HOLD:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState.HOLD
                ),
                diagnostic_code=decision.diagnostic_code,
                execute=False,
                confidence=policy.confidence,
                reason="Recovery decision requires manual intervention.",
            )

        if policy.state is ExperiencePolicyState.MANUAL_REQUIRED:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState.HOLD
                ),
                diagnostic_code=decision.diagnostic_code,
                execute=False,
                confidence=policy.confidence,
                reason="Recovery experience requires manual intervention.",
            )

        if not policy.allow_retry:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState.BLOCK
                ),
                diagnostic_code=decision.diagnostic_code,
                execute=False,
                confidence=policy.confidence,
                reason="Recovery experience does not permit another retry.",
            )

        return cls(
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState.ALLOW
            ),
            diagnostic_code=decision.diagnostic_code,
            execute=True,
            confidence=policy.confidence,
            reason="Recovery retry is permitted by experience policy.",
        )
