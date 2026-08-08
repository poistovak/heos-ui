from heos_ui.decision import (
    Action,
    BackoffPolicy,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
)
from heos_ui.decision.health_guard import HealthAwareDecisionGuard
from heos_ui.decision.recovery import RecoveryPolicy, RecoveryState
from heos_ui.diagnostics import HealthRegistry
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


def create_guard(
    threshold: int = 2,
) -> tuple[
    HealthAwareDecisionGuard,
    HealthRegistry,
    RecoveryPolicy,
    DecisionAuditTrail,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=threshold,
    )

    recovery = RecoveryPolicy(backoff)
    registry = HealthRegistry(recovery)
    guard = HealthAwareDecisionGuard(registry)

    return guard, registry, recovery, audit


def fail(
    audit: DecisionAuditTrail,
    target: str = "wattpilot",
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_healthy_target_is_allowed() -> None:
    guard, registry, _, _ = create_guard()
    registry.register("wattpilot")

    result = guard.evaluate(candidate())

    assert result.allowed
    assert result.state is RecoveryState.HEALTHY
    assert result.reason == "Target is healthy."


def test_allows_healthy_target() -> None:
    guard, registry, _, _ = create_guard()
    registry.register("wattpilot")

    assert guard.allows(candidate())


def test_unknown_target_is_blocked() -> None:
    guard, _, _, _ = create_guard()

    result = guard.evaluate(candidate())

    assert not result.allowed
    assert result.state is None
    assert result.reason == "Target is not registered."


def test_backoff_target_is_blocked() -> None:
    guard, registry, _, audit = create_guard()
    registry.register("wattpilot")

    fail(audit)
    fail(audit)

    result = guard.evaluate(candidate())

    assert not result.allowed
    assert result.state is RecoveryState.BACKOFF
    assert result.reason == "Target is in backoff."


def test_allows_returns_false_for_backoff() -> None:
    guard, registry, _, audit = create_guard()
    registry.register("wattpilot")

    fail(audit)
    fail(audit)

    assert not guard.allows(candidate())


def test_probe_target_is_blocked() -> None:
    guard, registry, recovery, audit = create_guard()
    registry.register("wattpilot")

    fail(audit)
    fail(audit)
    recovery.begin_probe("wattpilot")

    result = guard.evaluate(candidate())

    assert not result.allowed
    assert result.state is RecoveryState.PROBE
    assert result.reason == "Target is in recovery probe."


def test_targets_are_independent() -> None:
    guard, registry, _, audit = create_guard()

    registry.register("wattpilot")
    registry.register("daikin")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    assert not guard.allows(candidate("wattpilot"))
    assert guard.allows(candidate("daikin"))


def test_unregister_blocks_target() -> None:
    guard, registry, _, _ = create_guard()

    registry.register("wattpilot")
    registry.unregister("wattpilot")

    result = guard.evaluate(candidate())

    assert not result.allowed
    assert result.state is None
    assert result.reason == "Target is not registered."