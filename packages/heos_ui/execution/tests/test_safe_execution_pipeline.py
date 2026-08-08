from heos_ui.decision import (
    Action,
    BackoffPolicy,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    FeedbackEngine,
)
from heos_ui.decision.recovery import RecoveryPolicy
from heos_ui.energy import EnergySnapshot
from heos_ui.execution import ExecutionEngine, ExecutionSafetyGate
from heos_ui.execution.pipeline import SafeExecutionPipeline


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


def create_pipeline(
    threshold: int = 3,
) -> tuple[
    SafeExecutionPipeline,
    DecisionAuditTrail,
    FeedbackEngine,
    RecoveryPolicy,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=threshold,
    )

    recovery = RecoveryPolicy(backoff)

    gate = ExecutionSafetyGate(
        engine=ExecutionEngine(),
        recovery=recovery,
    )

    pipeline = SafeExecutionPipeline(
        gate=gate,
        audit=audit,
    )

    return pipeline, audit, feedback, recovery


def test_successful_execution_is_audited() -> None:
    pipeline, audit, _, _ = create_pipeline()

    result = pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=True,
        message="Executed.",
    )

    assert result.executed
    assert result.success
    assert audit.count == 1
    assert audit.successful()[0].outcome.message == "Executed."


def test_failed_execution_is_audited() -> None:
    pipeline, audit, _, _ = create_pipeline()

    result = pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
        message="Device unavailable.",
    )

    assert result.executed
    assert not result.success
    assert audit.count == 1
    assert len(audit.failed()) == 1


def test_failure_updates_feedback() -> None:
    pipeline, _, feedback, _ = create_pipeline()

    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    summary = feedback.summarize("wattpilot")

    assert summary.failed == 1
    assert summary.consecutive_failures == 1


def test_repeated_failures_trigger_backoff() -> None:
    pipeline, audit, _, recovery = create_pipeline(
        threshold=2,
    )

    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    assert audit.count == 2
    assert not recovery.can_execute("wattpilot")


def test_backoff_blocks_execution() -> None:
    pipeline, audit, _, _ = create_pipeline(
        threshold=2,
    )

    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    result = pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=True,
    )

    assert not result.executed
    assert not result.success
    assert result.message == "Target is in backoff."
    assert audit.count == 2


def test_targets_are_independent() -> None:
    pipeline, audit, _, _ = create_pipeline(
        threshold=2,
    )

    pipeline.execute(
        EnergySnapshot(),
        candidate("wattpilot"),
        success=False,
    )
    pipeline.execute(
        EnergySnapshot(),
        candidate("wattpilot"),
        success=False,
    )

    result = pipeline.execute(
        EnergySnapshot(),
        candidate("daikin"),
        success=True,
    )

    assert result.executed
    assert result.success
    assert audit.count == 3


def test_probe_can_pass_gate() -> None:
    pipeline, _, _, recovery = create_pipeline(
        threshold=2,
    )

    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    recovery.begin_probe("wattpilot")

    result = pipeline.execute(
        EnergySnapshot(),
        candidate(),
        success=True,
        message="Probe succeeded.",
    )

    assert result.executed
    assert result.success