import importlib

authorization_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "authorization"
)
gate_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "experience_gate"
)

Authorization = (
    authorization_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorization
)
AuthorizationState = (
    authorization_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState
)
Gate = (
    gate_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGate
)
GateState = (
    gate_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperienceGateState
)


def gate(
    *,
    state: GateState,
    code: str = "RUN_SYNC_MISMATCH",
    execute: bool,
    confidence: float = 0.75,
    reason: str = "gate",
) -> Gate:
    return Gate(
        state=state,
        diagnostic_code=code,
        execute=execute,
        confidence=confidence,
        reason=reason,
    )


def test_allow_gate_authorizes_execution() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            execute=True,
        )
    )

    assert authorization.state is AuthorizationState.AUTHORIZED


def test_authorized_state_sets_authorized_true() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            execute=True,
        )
    )

    assert authorization.authorized


def test_authorized_state_has_reason() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            execute=True,
        )
    )

    assert authorization.reason == "Recovery execution is authorized."


def test_block_gate_denies_execution() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.BLOCK,
            execute=False,
        )
    )

    assert authorization.state is AuthorizationState.DENIED


def test_denied_state_sets_authorized_false() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.BLOCK,
            execute=False,
        )
    )

    assert not authorization.authorized


def test_denied_state_has_reason() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.BLOCK,
            execute=False,
        )
    )

    assert authorization.reason == "Recovery execution is denied."


def test_hold_gate_requires_manual_authorization() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.HOLD,
            execute=False,
        )
    )

    assert authorization.state is AuthorizationState.MANUAL


def test_manual_state_is_not_authorized() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.HOLD,
            execute=False,
        )
    )

    assert not authorization.authorized


def test_manual_state_has_reason() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.HOLD,
            execute=False,
        )
    )

    assert authorization.reason == (
        "Recovery execution requires manual authorization."
    )


def test_authorization_preserves_diagnostic_code() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            code="RUN_STATUS_COUNT_MISMATCH",
            execute=True,
        )
    )

    assert authorization.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_authorization_preserves_allow_confidence() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            execute=True,
            confidence=0.82,
        )
    )

    assert authorization.confidence == 0.82


def test_authorization_preserves_block_confidence() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.BLOCK,
            execute=False,
            confidence=0.91,
        )
    )

    assert authorization.confidence == 0.91


def test_authorization_preserves_hold_confidence() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.HOLD,
            execute=False,
            confidence=1.0,
        )
    )

    assert authorization.confidence == 1.0


def test_zero_confidence_can_be_authorized() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            execute=True,
            confidence=0.0,
        )
    )

    assert authorization.state is AuthorizationState.AUTHORIZED
    assert authorization.authorized
    assert authorization.confidence == 0.0


def test_block_never_authorizes_execution() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.BLOCK,
            execute=False,
            confidence=1.0,
        )
    )

    assert not authorization.authorized


def test_hold_never_authorizes_execution() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.HOLD,
            execute=False,
            confidence=1.0,
        )
    )

    assert not authorization.authorized


def test_authorization_is_stable_snapshot() -> None:
    authorization = Authorization.from_gate(
        gate(
            state=GateState.ALLOW,
            code="RUN_SYNC_MISMATCH",
            execute=True,
            confidence=0.6,
        )
    )

    assert authorization.state is AuthorizationState.AUTHORIZED
    assert authorization.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert authorization.authorized
    assert authorization.confidence == 0.6
