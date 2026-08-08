import pytest
from heos_ui.decision import (
    Action,
    BackoffPolicy,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
)
from heos_ui.decision.recovery import (
    RecoveryPolicy,
    RecoveryState,
)
from heos_ui.diagnostics.health_registry import (
    HealthRegistry,
    SystemHealth,
)
from heos_ui.energy import EnergySnapshot


def candidate(
    target: str,
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target=target,
            action="set_current",
            reason="Health registry test.",
        ),
        action=Action(
            priority=100,
            target=target,
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def create_registry(
    threshold: int = 2,
) -> tuple[
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

    return registry, recovery, audit


def fail(
    audit: DecisionAuditTrail,
    target: str,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_register_target() -> None:
    registry, _, _ = create_registry()

    registry.register("wattpilot")

    assert registry.contains("wattpilot")
    assert registry.count == 1


def test_duplicate_registration_is_idempotent() -> None:
    registry, _, _ = create_registry()

    registry.register("wattpilot")
    registry.register("wattpilot")

    assert registry.count == 1


def test_empty_target_is_rejected() -> None:
    registry, _, _ = create_registry()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        registry.register("")


def test_unregister_target() -> None:
    registry, _, _ = create_registry()

    registry.register("wattpilot")
    registry.unregister("wattpilot")

    assert not registry.contains("wattpilot")
    assert registry.count == 0


def test_unknown_target_health_is_rejected() -> None:
    registry, _, _ = create_registry()

    with pytest.raises(KeyError):
        registry.health("wattpilot")


def test_registered_target_starts_healthy() -> None:
    registry, _, _ = create_registry()

    registry.register("wattpilot")

    result = registry.health("wattpilot")

    assert result.target == "wattpilot"
    assert result.state is RecoveryState.HEALTHY


def test_snapshot_is_sorted() -> None:
    registry, _, _ = create_registry()

    registry.register("wattpilot")
    registry.register("daikin")
    registry.register("fronius")

    snapshot = registry.snapshot()

    assert tuple(
        item.target for item in snapshot
    ) == (
        "daikin",
        "fronius",
        "wattpilot",
    )


def test_system_is_healthy_when_targets_are_healthy() -> None:
    registry, _, _ = create_registry()

    registry.register("wattpilot")
    registry.register("fronius")
    registry.register("daikin")

    assert registry.system_health is SystemHealth.HEALTHY


def test_backoff_makes_system_degraded() -> None:
    registry, _, audit = create_registry()

    registry.register("wattpilot")
    registry.register("fronius")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    assert (
        registry.health("wattpilot").state
        is RecoveryState.BACKOFF
    )
    assert registry.system_health is SystemHealth.DEGRADED


def test_probe_makes_system_degraded() -> None:
    registry, recovery, audit = create_registry()

    registry.register("wattpilot")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    recovery.begin_probe("wattpilot")

    assert (
        registry.health("wattpilot").state
        is RecoveryState.PROBE
    )
    assert registry.system_health is SystemHealth.DEGRADED


def test_unhealthy_returns_only_non_healthy_targets() -> None:
    registry, _, audit = create_registry()

    registry.register("wattpilot")
    registry.register("fronius")
    registry.register("daikin")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    unhealthy = registry.unhealthy()

    assert len(unhealthy) == 1
    assert unhealthy[0].target == "wattpilot"
    assert unhealthy[0].state is RecoveryState.BACKOFF