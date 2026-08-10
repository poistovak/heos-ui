import importlib

import pytest

decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)
gate_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "experience_gate"
)
policy_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "experience_policy"
)

Decision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)
DecisionState = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
)
Gate = (
    gate_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGate
)
GateState = (
    gate_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState
)
Policy = (
    policy_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicy
)
PolicyState = (
    policy_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState
)


def decision(
    *,
    state: DecisionState = DecisionState.RETRY,
    code: str = "RUN_SYNC_MISMATCH",
    execute: bool = True,
) -> Decision:
    return Decision(
        state=state,
        diagnostic_code=code,
        execute=execute,
        reason="decision",
        action="action",
    )


def policy(
    *,
    state: PolicyState = PolicyState.RETRY_SUPPORTED,
    code: str = "RUN_SYNC_MISMATCH",
    allow_retry: bool = True,
    confidence: float = 0.75,
) -> Policy:
    return Policy(
        diagnostic_code=code,
        state=state,
        allow_retry=allow_retry,
        confidence=confidence,
        reason="policy",
    )


def test_supported_retry_is_allowed() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(),
    )

    assert gate.state is GateState.ALLOW
    assert gate.execute


def test_allowed_retry_preserves_confidence() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(confidence=0.8),
    )

    assert gate.confidence == 0.8


def test_cold_start_allows_retry() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            state=PolicyState.COLD_START,
            confidence=0.0,
        ),
    )

    assert gate.state is GateState.ALLOW
    assert gate.execute


def test_discouraged_retry_is_blocked() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            state=PolicyState.RETRY_DISCOURAGED,
            allow_retry=False,
        ),
    )

    assert gate.state is GateState.BLOCK
    assert not gate.execute


def test_discouraged_retry_has_reason() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            state=PolicyState.RETRY_DISCOURAGED,
            allow_retry=False,
        ),
    )

    assert gate.reason == (
        "Recovery experience does not permit another retry."
    )


def test_manual_policy_holds_recovery() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            state=PolicyState.MANUAL_REQUIRED,
            allow_retry=False,
            confidence=1.0,
        ),
    )

    assert gate.state is GateState.HOLD
    assert not gate.execute


def test_manual_policy_has_reason() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            state=PolicyState.MANUAL_REQUIRED,
            allow_retry=False,
            confidence=1.0,
        ),
    )

    assert gate.reason == (
        "Recovery experience requires manual intervention."
    )


def test_skip_decision_is_blocked() -> None:
    gate = Gate.evaluate(
        decision(
            state=DecisionState.SKIP,
            execute=False,
        ),
        policy(),
    )

    assert gate.state is GateState.BLOCK
    assert not gate.execute


def test_skip_decision_has_reason() -> None:
    gate = Gate.evaluate(
        decision(
            state=DecisionState.SKIP,
            execute=False,
        ),
        policy(),
    )

    assert gate.reason == (
        "Recovery decision does not require execution."
    )


def test_hold_decision_remains_held() -> None:
    gate = Gate.evaluate(
        decision(
            state=DecisionState.HOLD,
            execute=False,
        ),
        policy(),
    )

    assert gate.state is GateState.HOLD
    assert not gate.execute


def test_hold_decision_has_reason() -> None:
    gate = Gate.evaluate(
        decision(
            state=DecisionState.HOLD,
            execute=False,
        ),
        policy(),
    )

    assert gate.reason == (
        "Recovery decision requires manual intervention."
    )


def test_gate_preserves_diagnostic_code() -> None:
    gate = Gate.evaluate(
        decision(
            code="RUN_STATUS_COUNT_MISMATCH",
        ),
        policy(
            code="RUN_STATUS_COUNT_MISMATCH",
        ),
    )

    assert gate.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_mismatched_codes_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Recovery decision and experience policy codes "
            "do not match."
        ),
    ):
        Gate.evaluate(
            decision(
                code="RUN_SYNC_MISMATCH",
            ),
            policy(
                code="RUN_STATUS_COUNT_MISMATCH",
            ),
        )


def test_allowed_retry_has_reason() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(),
    )

    assert gate.reason == (
        "Recovery retry is permitted by experience policy."
    )


def test_cold_start_has_zero_confidence() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            state=PolicyState.COLD_START,
            confidence=0.0,
        ),
    )

    assert gate.confidence == 0.0


def test_manual_policy_overrides_retry_decision() -> None:
    gate = Gate.evaluate(
        decision(
            state=DecisionState.RETRY,
            execute=True,
        ),
        policy(
            state=PolicyState.MANUAL_REQUIRED,
            allow_retry=False,
            confidence=1.0,
        ),
    )

    assert gate.state is GateState.HOLD
    assert not gate.execute


def test_gate_is_stable_snapshot() -> None:
    gate = Gate.evaluate(
        decision(),
        policy(
            confidence=0.6,
        ),
    )

    assert gate.state is GateState.ALLOW
    assert gate.execute
    assert gate.confidence == 0.6
