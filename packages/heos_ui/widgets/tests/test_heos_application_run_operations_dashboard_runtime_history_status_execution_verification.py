import importlib

completion_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_completion"
)
verification_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "execution_verification"
)

Completion = (
    completion_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletion
)
CompletionState = (
    completion_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionCompletionState
)
Verification = (
    verification_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerification
)
VerificationState = (
    verification_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExecutionVerificationState
)


def completion(
    *,
    sequence: int = 1,
    state: CompletionState = CompletionState.COMPLETED,
    code: str = "RUN_SYNC_MISMATCH",
    action: str = "Retry synchronization.",
    completed: bool = True,
    confidence: float = 0.75,
) -> Completion:
    return Completion(
        sequence=sequence,
        state=state,
        diagnostic_code=code,
        action=action,
        completed=completed,
        confidence=confidence,
        reason="completion",
    )


def test_successful_observation_is_verified() -> None:
    verification = Verification.verify(
        completion(),
        observed_success=True,
    )

    assert verification.state is VerificationState.VERIFIED


def test_verified_state_sets_verified_true() -> None:
    verification = Verification.verify(
        completion(),
        observed_success=True,
    )

    assert verification.verified


def test_verified_state_has_reason() -> None:
    verification = Verification.verify(
        completion(),
        observed_success=True,
    )

    assert verification.reason == (
        "Recovery execution produced the expected result."
    )


def test_unsuccessful_observation_fails_verification() -> None:
    verification = Verification.verify(
        completion(),
        observed_success=False,
    )

    assert verification.state is VerificationState.FAILED


def test_failed_verification_sets_verified_false() -> None:
    verification = Verification.verify(
        completion(),
        observed_success=False,
    )

    assert not verification.verified


def test_failed_verification_has_reason() -> None:
    verification = Verification.verify(
        completion(),
        observed_success=False,
    )

    assert verification.reason == (
        "Recovery execution did not produce the expected result."
    )


def test_not_started_completion_is_not_completed() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.NOT_STARTED,
            completed=False,
        ),
        observed_success=True,
    )

    assert verification.state is VerificationState.NOT_COMPLETED


def test_not_completed_is_not_verified() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.NOT_STARTED,
            completed=False,
        ),
        observed_success=True,
    )

    assert not verification.verified


def test_not_completed_has_reason() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.NOT_STARTED,
            completed=False,
        ),
        observed_success=True,
    )

    assert verification.reason == (
        "Recovery execution was not completed."
    )


def test_manual_completion_remains_manual() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.MANUAL,
            completed=False,
        ),
        observed_success=True,
    )

    assert verification.state is VerificationState.MANUAL


def test_manual_verification_is_false() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.MANUAL,
            completed=False,
        ),
        observed_success=True,
    )

    assert not verification.verified


def test_manual_verification_has_reason() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.MANUAL,
            completed=False,
        ),
        observed_success=True,
    )

    assert verification.reason == (
        "Recovery execution verification requires manual handling."
    )


def test_completed_state_without_completed_flag_is_not_completed() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.COMPLETED,
            completed=False,
        ),
        observed_success=True,
    )

    assert verification.state is VerificationState.NOT_COMPLETED
    assert not verification.verified


def test_verification_preserves_sequence() -> None:
    verification = Verification.verify(
        completion(sequence=16),
        observed_success=True,
    )

    assert verification.sequence == 16


def test_verification_preserves_diagnostic_code() -> None:
    verification = Verification.verify(
        completion(
            code="RUN_STATUS_COUNT_MISMATCH",
        ),
        observed_success=True,
    )

    assert verification.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_verification_preserves_action() -> None:
    verification = Verification.verify(
        completion(
            action="Retry status generation.",
        ),
        observed_success=True,
    )

    assert verification.action == "Retry status generation."


def test_verification_preserves_confidence() -> None:
    verification = Verification.verify(
        completion(
            confidence=0.95,
        ),
        observed_success=True,
    )

    assert verification.confidence == 0.95


def test_zero_confidence_is_preserved() -> None:
    verification = Verification.verify(
        completion(
            confidence=0.0,
        ),
        observed_success=True,
    )

    assert verification.confidence == 0.0


def test_failed_snapshot_preserves_identity() -> None:
    verification = Verification.verify(
        completion(
            sequence=12,
            code="RUN_SYNC_MISMATCH",
            action="Retry synchronization.",
            confidence=0.69,
        ),
        observed_success=False,
    )

    assert verification.sequence == 12
    assert verification.diagnostic_code == "RUN_SYNC_MISMATCH"
    assert verification.action == "Retry synchronization."
    assert verification.confidence == 0.69


def test_observed_success_cannot_override_not_completed() -> None:
    verification = Verification.verify(
        completion(
            state=CompletionState.NOT_STARTED,
            completed=False,
        ),
        observed_success=True,
    )

    assert verification.state is VerificationState.NOT_COMPLETED
    assert not verification.verified
