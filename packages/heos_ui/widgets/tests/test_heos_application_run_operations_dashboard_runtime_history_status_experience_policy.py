import importlib

experience_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_experience"
)
policy_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "experience_policy"
)

Experience = (
    experience_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryExperience
)
Policy = (
    policy_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicy
)
PolicyState = (
    policy_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusExperiencePolicyState
)


def experience(
    *,
    code: str = "RUN_SYNC_MISMATCH",
    observations: int = 0,
    positive: int = 0,
    negative: int = 0,
    manual: int = 0,
    success_rate: float | None = None,
    retry_supported: bool = False,
) -> Experience:
    return Experience(
        diagnostic_code=code,
        observations=observations,
        positive=positive,
        negative=negative,
        manual=manual,
        success_rate=success_rate,
        retry_supported=retry_supported,
    )


def test_empty_experience_is_cold_start() -> None:
    policy = Policy.evaluate(
        experience()
    )

    assert policy.state is PolicyState.COLD_START


def test_cold_start_allows_retry() -> None:
    policy = Policy.evaluate(
        experience()
    )

    assert policy.allow_retry


def test_cold_start_has_zero_confidence() -> None:
    policy = Policy.evaluate(
        experience()
    )

    assert policy.confidence == 0.0


def test_cold_start_has_reason() -> None:
    policy = Policy.evaluate(
        experience()
    )

    assert policy.reason == "No recovery experience is available yet."


def test_manual_history_requires_manual_policy() -> None:
    policy = Policy.evaluate(
        experience(
            observations=2,
            manual=1,
        )
    )

    assert policy.state is PolicyState.MANUAL_REQUIRED


def test_manual_policy_blocks_retry() -> None:
    policy = Policy.evaluate(
        experience(
            observations=2,
            manual=1,
        )
    )

    assert not policy.allow_retry


def test_manual_policy_has_full_confidence() -> None:
    policy = Policy.evaluate(
        experience(
            observations=2,
            manual=1,
        )
    )

    assert policy.confidence == 1.0


def test_supported_history_allows_retry() -> None:
    policy = Policy.evaluate(
        experience(
            observations=3,
            positive=2,
            negative=1,
            success_rate=2 / 3,
            retry_supported=True,
        )
    )

    assert policy.state is PolicyState.RETRY_SUPPORTED
    assert policy.allow_retry


def test_supported_policy_uses_success_rate_as_confidence() -> None:
    policy = Policy.evaluate(
        experience(
            observations=4,
            positive=3,
            negative=1,
            success_rate=0.75,
            retry_supported=True,
        )
    )

    assert policy.confidence == 0.75


def test_supported_policy_has_reason() -> None:
    policy = Policy.evaluate(
        experience(
            observations=2,
            negative=1,
            positive=1,
            success_rate=0.5,
            retry_supported=True,
        )
    )

    assert policy.reason == "Historical recovery supports another retry."


def test_unsupported_history_discourages_retry() -> None:
    policy = Policy.evaluate(
        experience(
            observations=2,
            positive=2,
            success_rate=1.0,
            retry_supported=False,
        )
    )

    assert policy.state is PolicyState.RETRY_DISCOURAGED
    assert not policy.allow_retry


def test_discouraged_policy_uses_inverse_success_rate() -> None:
    policy = Policy.evaluate(
        experience(
            observations=4,
            positive=1,
            negative=3,
            success_rate=0.25,
            retry_supported=False,
        )
    )

    assert policy.confidence == 0.75


def test_discouraged_policy_handles_missing_success_rate() -> None:
    policy = Policy.evaluate(
        experience(
            observations=1,
            manual=0,
            success_rate=None,
            retry_supported=False,
        )
    )

    assert policy.state is PolicyState.RETRY_DISCOURAGED
    assert policy.confidence == 0.0


def test_manual_history_overrides_retry_support() -> None:
    policy = Policy.evaluate(
        experience(
            observations=3,
            positive=1,
            negative=1,
            manual=1,
            success_rate=0.5,
            retry_supported=True,
        )
    )

    assert policy.state is PolicyState.MANUAL_REQUIRED
    assert not policy.allow_retry


def test_policy_preserves_diagnostic_code() -> None:
    policy = Policy.evaluate(
        experience(
            code="RUN_STATUS_COUNT_MISMATCH",
        )
    )

    assert policy.diagnostic_code == "RUN_STATUS_COUNT_MISMATCH"


def test_policy_is_snapshot() -> None:
    source = experience(
        observations=3,
        positive=2,
        negative=1,
        success_rate=2 / 3,
        retry_supported=True,
    )

    policy = Policy.evaluate(source)

    assert policy.state is PolicyState.RETRY_SUPPORTED
    assert policy.allow_retry
    assert policy.confidence == 2 / 3


def test_discouraged_policy_has_reason() -> None:
    policy = Policy.evaluate(
        experience(
            observations=1,
            negative=1,
            success_rate=0.0,
            retry_supported=False,
        )
    )

    assert policy.reason == (
        "Historical recovery does not support another retry."
    )
