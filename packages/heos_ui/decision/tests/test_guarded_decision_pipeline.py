from heos_ui.decision import (
    Action,
    ActionQueue,
    BackoffPolicy,
    ConflictResolver,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
    HealthAwareDecisionGuard,
)
from heos_ui.decision.guarded_pipeline import GuardedDecisionPipeline
from heos_ui.decision.recovery import RecoveryPolicy
from heos_ui.diagnostics import HealthRegistry
from heos_ui.energy import EnergySnapshot


def candidate(
    target: str = "wattpilot",
    *,
    priority: int = 100,
    command: str = "set_current",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=priority,
            target=target,
            action=command,
            reason="Policy matched.",
        ),
        action=Action(
            priority=priority,
            target=target,
            command=command,
            parameters={"amps": 16},
        ),
    )


def create_pipeline(
    threshold: int = 2,
) -> tuple[
    GuardedDecisionPipeline,
    HealthRegistry,
    DecisionAuditTrail,
    ActionQueue,
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
    actions = ActionQueue()

    pipeline = GuardedDecisionPipeline(
        resolver=ConflictResolver(),
        guard=guard,
        actions=actions,
    )

    return pipeline, registry, audit, actions


def fail(
    audit: DecisionAuditTrail,
    target: str,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_empty_candidates() -> None:
    pipeline, _, _, actions = create_pipeline()

    result = pipeline.process([])

    assert result.accepted == ()
    assert result.blocked == ()
    assert actions.count == 0


def test_healthy_candidate_is_accepted() -> None:
    pipeline, registry, _, actions = create_pipeline()

    registry.register("wattpilot")

    result = pipeline.process(
        [candidate()]
    )

    assert len(result.accepted) == 1
    assert result.blocked == ()
    assert actions.count == 1


def test_unknown_target_is_blocked() -> None:
    pipeline, _, _, actions = create_pipeline()

    result = pipeline.process(
        [candidate()]
    )

    assert result.accepted == ()
    assert len(result.blocked) == 1
    assert result.blocked[0].reason == (
        "Target is not registered."
    )
    assert actions.count == 0


def test_backoff_target_is_blocked() -> None:
    pipeline, registry, audit, actions = create_pipeline()

    registry.register("wattpilot")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    result = pipeline.process(
        [candidate()]
    )

    assert result.accepted == ()
    assert len(result.blocked) == 1
    assert result.blocked[0].reason == (
        "Target is in backoff."
    )
    assert actions.count == 0


def test_conflict_resolver_selects_highest_priority() -> None:
    pipeline, registry, _, actions = create_pipeline()

    registry.register("wattpilot")

    low = candidate(
        priority=10,
        command="set_current",
    )
    high = candidate(
        priority=100,
        command="stop",
    )

    result = pipeline.process(
        [
            low,
            high,
        ]
    )

    assert result.accepted == (high,)
    assert actions.count == 1
    assert actions.peek() == high.action


def test_different_healthy_targets_are_queued() -> None:
    pipeline, registry, _, actions = create_pipeline()

    registry.register("wattpilot")
    registry.register("daikin")

    result = pipeline.process(
        [
            candidate(
                "wattpilot",
                priority=100,
            ),
            candidate(
                "daikin",
                priority=50,
            ),
        ]
    )

    assert len(result.accepted) == 2
    assert result.blocked == ()
    assert actions.count == 2


def test_healthy_and_unhealthy_targets_are_separated() -> None:
    pipeline, registry, audit, actions = create_pipeline()

    registry.register("wattpilot")
    registry.register("daikin")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    result = pipeline.process(
        [
            candidate("wattpilot"),
            candidate("daikin"),
        ]
    )

    assert len(result.accepted) == 1
    assert result.accepted[0].action.target == "daikin"

    assert len(result.blocked) == 1
    assert (
        result.blocked[0].candidate.action.target
        == "wattpilot"
    )

    assert actions.count == 1