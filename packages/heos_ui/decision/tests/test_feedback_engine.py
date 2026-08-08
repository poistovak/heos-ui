import pytest
from heos_ui.decision import (
    Action,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
)
from heos_ui.decision.feedback import FeedbackEngine
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


def record_outcome(
    audit: DecisionAuditTrail,
    *,
    target: str = "wattpilot",
    success: bool,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=success),
    )


def test_empty_feedback() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    summary = engine.summarize("wattpilot")

    assert summary.total == 0
    assert summary.successful == 0
    assert summary.failed == 0
    assert summary.success_rate == 0.0
    assert summary.healthy


def test_successful_outcome() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(
        audit,
        success=True,
    )

    summary = engine.summarize("wattpilot")

    assert summary.total == 1
    assert summary.successful == 1
    assert summary.failed == 0
    assert summary.success_rate == 1.0


def test_failed_outcome() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(
        audit,
        success=False,
    )

    summary = engine.summarize("wattpilot")

    assert summary.total == 1
    assert summary.failed == 1
    assert summary.success_rate == 0.0
    assert not summary.healthy


def test_success_rate() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(audit, success=True)
    record_outcome(audit, success=True)
    record_outcome(audit, success=False)

    summary = engine.summarize("wattpilot")

    assert summary.total == 3
    assert summary.successful == 2
    assert summary.failed == 1
    assert summary.success_rate == pytest.approx(
        2 / 3
    )


def test_failure_streak() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(audit, success=True)
    record_outcome(audit, success=False)
    record_outcome(audit, success=False)

    summary = engine.summarize("wattpilot")

    assert summary.consecutive_failures == 2


def test_success_resets_failure_streak() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(audit, success=False)
    record_outcome(audit, success=False)
    record_outcome(audit, success=True)

    summary = engine.summarize("wattpilot")

    assert summary.consecutive_failures == 0
    assert summary.healthy


def test_feedback_isolated_by_target() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(
        audit,
        target="wattpilot",
        success=False,
    )
    record_outcome(
        audit,
        target="daikin",
        success=True,
    )

    wattpilot = engine.summarize("wattpilot")
    daikin = engine.summarize("daikin")

    assert wattpilot.failed == 1
    assert daikin.successful == 1


def test_should_back_off_after_threshold() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(audit, success=False)
    record_outcome(audit, success=False)
    record_outcome(audit, success=False)

    assert engine.should_back_off("wattpilot")


def test_should_not_back_off_below_threshold() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    record_outcome(audit, success=False)
    record_outcome(audit, success=False)

    assert not engine.should_back_off("wattpilot")


def test_invalid_failure_threshold() -> None:
    audit = DecisionAuditTrail()
    engine = FeedbackEngine(audit)

    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        engine.should_back_off(
            "wattpilot",
            failure_threshold=0,
        )