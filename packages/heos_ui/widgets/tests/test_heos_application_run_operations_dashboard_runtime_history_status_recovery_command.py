import importlib

import pytest

authorization_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "authorization"
)
command_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_command"
)
decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)

Authorization = (
    authorization_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorization
)
AuthorizationState = (
    authorization_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState
)
Command = (
    command_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommand
)
CommandState = (
    command_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState
)
Decision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)
DecisionState = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
)


def decision(
    *,
    code: str = "RUN_SYNC_MISMATCH",
    execute: bool = True,
    action: str = "Retry synchronization.",
) -> Decision:
    return Decision(
        state=DecisionState.RETRY,
        diagnostic_code=code,
        execute=execute,
        reason="decision",
        action=action,
    )


def authorization(
    *,
    state: AuthorizationState = AuthorizationState.AUTHORIZED,
    code: str = "RUN_SYNC_MISMATCH",
    authorized: bool = True,
    confidence: float = 0.75,
) -> Authorization:
    return Authorization(
        state=state,
        diagnostic_code=code,
        authorized=authorized,
        confidence=confidence,
        reason="authorization",
    )


def test_authorized_decision_builds_ready_command() -> None:
    command = Command.build(
        decision(),
        authorization(),
    )

    assert command.state is CommandState.READY


def test_ready_command_is_executable() -> None:
    command = Command.build(
        decision(),
        authorization(),
    )

    assert command.executable


def test_ready_command_has_reason() -> None:
    command = Command.build(
        decision(),
        authorization(),
    )

    assert command.reason == "Recovery command is ready for execution."


def test_denied_authorization_builds_blocked_command() -> None:
    command = Command.build(
        decision(),
        authorization(
            state=AuthorizationState.DENIED,
            authorized=False,
        ),
    )

    assert command.state is CommandState.BLOCKED


def test_denied_command_is_not_executable() -> None:
    command = Command.build(
        decision(),
        authorization(
            state=AuthorizationState.DENIED,
            authorized=False,
        ),
    )

    assert not command.executable


def test_denied_command_has_reason() -> None:
    command = Command.build(
        decision(),
        authorization(
            state=AuthorizationState.DENIED,
            authorized=False,
        ),
    )

    assert command.reason == (
        "Recovery command is blocked by authorization."
    )


def test_manual_authorization_builds_manual_command() -> None:
    command = Command.build(
        decision(),
        authorization(
            state=AuthorizationState.MANUAL,
            authorized=False,
            confidence=1.0,
        ),
    )

    assert command.state is CommandState.MANUAL


def test_manual_command_is_not_executable() -> None:
    command = Command.build(
        decision(),
        authorization(
            state=AuthorizationState.MANUAL,
            authorized=False,
            confidence=1.0,
        ),
    )

    assert not command.executable


def test_manual_command_has_reason() -> None:
    command = Command.build(
        decision(),
        authorization(
            state=AuthorizationState.MANUAL,
            authorized=False,
            confidence=1.0,
        ),
    )

    assert command.reason == (
        "Recovery command requires manual authorization."
    )


def test_non_executable_decision_is_blocked() -> None:
    command = Command.build(
        decision(
            execute=False,
        ),
        authorization(),
    )

    assert command.state is CommandState.BLOCKED
    assert not command.executable


def test_non_executable_decision_has_reason() -> None:
    command = Command.build(
        decision(
            execute=False,
        ),
        authorization(),
    )

    assert command.reason == (
        "Recovery decision does not permit execution."
    )


def test_command_preserves_diagnostic_code() -> None:
    command = Command.build(
        decision(
            code="RUN_STATUS_COUNT_MISMATCH",
        ),
        authorization(
            code="RUN_STATUS_COUNT_MISMATCH",
        ),
    )

    assert command.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_command_preserves_action() -> None:
    command = Command.build(
        decision(
            action="Retry status generation.",
        ),
        authorization(),
    )

    assert command.action == "Retry status generation."


def test_command_preserves_confidence() -> None:
    command = Command.build(
        decision(),
        authorization(
            confidence=0.84,
        ),
    )

    assert command.confidence == 0.84


def test_zero_confidence_authorization_can_build_ready_command() -> None:
    command = Command.build(
        decision(),
        authorization(
            confidence=0.0,
        ),
    )

    assert command.state is CommandState.READY
    assert command.executable
    assert command.confidence == 0.0


def test_mismatched_codes_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Recovery decision and authorization codes "
            "do not match."
        ),
    ):
        Command.build(
            decision(
                code="RUN_SYNC_MISMATCH",
            ),
            authorization(
                code="RUN_STATUS_COUNT_MISMATCH",
            ),
        )


def test_command_is_stable_snapshot() -> None:
    command = Command.build(
        decision(
            action="Retry synchronization.",
        ),
        authorization(
            confidence=0.6,
        ),
    )

    assert command.state is CommandState.READY
    assert command.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert command.action == "Retry synchronization."
    assert command.executable
    assert command.confidence == 0.6
