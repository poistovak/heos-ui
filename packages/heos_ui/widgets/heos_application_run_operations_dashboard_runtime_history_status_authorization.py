from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

gate_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "experience_gate"
)

ExperienceGate = (
    gate_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGate
)
ExperienceGateState = (
    gate_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState(
    str,
    Enum,
):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorization:
    state: HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState
    diagnostic_code: str
    authorized: bool
    confidence: float
    reason: str

    @classmethod
    def from_gate(
        cls,
        gate: ExperienceGate,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorization:
        if gate.state is ExperienceGateState.ALLOW:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState.AUTHORIZED
                ),
                diagnostic_code=gate.diagnostic_code,
                authorized=True,
                confidence=gate.confidence,
                reason="Recovery execution is authorized.",
            )

        if gate.state is ExperienceGateState.HOLD:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState.MANUAL
                ),
                diagnostic_code=gate.diagnostic_code,
                authorized=False,
                confidence=gate.confidence,
                reason="Recovery execution requires manual authorization.",
            )

        return cls(
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState.DENIED
            ),
            diagnostic_code=gate.diagnostic_code,
            authorized=False,
            confidence=gate.confidence,
            reason="Recovery execution is denied.",
        )
