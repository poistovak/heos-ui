import pytest
from heos_ui.decision import (
    Action,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
)
from heos_ui.decision.backoff import BackoffPolicy
from heos_ui.energy import EnergySnapshot


def candidate(
    target: str = "wattpilot",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target=target,
            action="set_current",
            reason="PV surplus available.",
        ),
        action=Action(
            priority=100,
            target=target,
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def record(
    audit: DecisionAuditTrail,
    *,
    success: bool,
    target: str = "wattpilot",
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=success),
    )


def create_policy(
    threshold: int = 3,
) -> tuple[
    BackoffPolicy,
    DecisionAuditTrail,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    return (
        BackoffPolicy(
            feedback=feedback,
            failure_threshold=threshold,
        ),
        audit,
    )


def test_allows_healthy_target() -> None:
    policy, _ = create_policy()

    assert policy.allows("wattpilot")


def test_blocks_after_failure_threshold() -> None:
    policy, audit = create_policy()

    record(audit, success=False)
    record(audit, success=False)
    record(audit, success=False)

    result = policy.evaluate("wattpilot")

    assert result.blocked
    assert result.failure_streak == 3
    assert not policy.allows("wattpilot")


def test_below_threshold_is_allowed() -> None:
    policy, audit = create_policy()

    record(audit, success=False)
    record(audit, success=False)

    assert policy.allows("wattpilot")


def test_success_resets_backoff() -> None:
    policy, audit = create_policy()

    record(audit, success=False)
    record(audit, success=False)
    record(audit, success=False)

    assert not policy.allows("wattpilot")

    record(audit, success=True)

    assert policy.allows("wattpilot")


def test_targets_are_independent() -> None:
    policy, audit = create_policy(
        threshold=2,
    )

    record(
        audit,
        target="wattpilot",
        success=False,
    )
    record(
        audit,
        target="wattpilot",
        success=False,
    )
    record(
        audit,
        target="daikin",
        success=True,
    )

    assert not policy.allows("wattpilot")
    assert policy.allows("daikin")


def test_custom_threshold() -> None:
    policy, audit = create_policy(
        threshold=2,
    )

    record(audit, success=False)
    assert policy.allows("wattpilot")

    record(audit, success=False)
    assert not policy.allows("wattpilot")


def test_invalid_threshold() -> None:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        BackoffPolicy(
            feedback=feedback,
            failure_threshold=0,
        )