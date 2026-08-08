from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_health import (
    BrainRuntimeHealthLevel,
    BrainRuntimeHealthSnapshot,
)
from heos_ui.widgets.brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)
from heos_ui.widgets.brain_runtime_recovery import (
    BrainRuntimeRecovery,
    BrainRuntimeRecoveryAction,
    BrainRuntimeRecoveryPolicy,
)
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def health(
    level: BrainRuntimeHealthLevel,
) -> BrainRuntimeHealthSnapshot:
    return BrainRuntimeHealthSnapshot(
        level=level,
        total_states=10,
        attention_states=0,
        attention_ratio=0.0,
        latest_cycle=174,
    )


def lifecycle() -> BrainRuntimeLifecycle:
    runtime = BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )
    runtime.start()
    return runtime


def test_unknown_health_waits() -> None:
    decision = BrainRuntimeRecoveryPolicy().decide(
        health(BrainRuntimeHealthLevel.UNKNOWN)
    )

    assert decision.action is BrainRuntimeRecoveryAction.WAIT
    assert not decision.can_continue
    assert not decision.should_stop


def test_healthy_health_continues() -> None:
    decision = BrainRuntimeRecoveryPolicy().decide(
        health(BrainRuntimeHealthLevel.HEALTHY)
    )

    assert decision.action is BrainRuntimeRecoveryAction.CONTINUE
    assert decision.can_continue
    assert not decision.should_stop


def test_degraded_health_continues_with_caution() -> None:
    decision = BrainRuntimeRecoveryPolicy().decide(
        health(BrainRuntimeHealthLevel.DEGRADED)
    )

    assert (
        decision.action
        is BrainRuntimeRecoveryAction.CONTINUE_WITH_CAUTION
    )
    assert decision.can_continue
    assert not decision.should_stop


def test_critical_health_stops() -> None:
    decision = BrainRuntimeRecoveryPolicy().decide(
        health(BrainRuntimeHealthLevel.CRITICAL)
    )

    assert decision.action is BrainRuntimeRecoveryAction.STOP
    assert decision.should_stop
    assert not decision.can_continue


def test_healthy_apply_keeps_runtime_started() -> None:
    runtime = lifecycle()

    recovery = BrainRuntimeRecovery(
        runtime=runtime,
        policy=BrainRuntimeRecoveryPolicy(),
    )

    recovery.apply(
        health(BrainRuntimeHealthLevel.HEALTHY)
    )

    assert runtime.state is BrainRuntimeLifecycleState.STARTED


def test_degraded_apply_keeps_runtime_active() -> None:
    runtime = lifecycle()

    recovery = BrainRuntimeRecovery(
        runtime=runtime,
        policy=BrainRuntimeRecoveryPolicy(),
    )

    decision = recovery.apply(
        health(BrainRuntimeHealthLevel.DEGRADED)
    )

    assert decision.can_continue
    assert runtime.started
    assert not runtime.stopped


def test_critical_apply_stops_runtime() -> None:
    runtime = lifecycle()

    recovery = BrainRuntimeRecovery(
        runtime=runtime,
        policy=BrainRuntimeRecoveryPolicy(),
    )

    decision = recovery.apply(
        health(BrainRuntimeHealthLevel.CRITICAL)
    )

    assert decision.should_stop
    assert runtime.state is BrainRuntimeLifecycleState.STOPPED


def test_recovery_returns_policy_reason() -> None:
    runtime = lifecycle()

    recovery = BrainRuntimeRecovery(
        runtime=runtime,
        policy=BrainRuntimeRecoveryPolicy(),
    )

    decision = recovery.apply(
        health(BrainRuntimeHealthLevel.CRITICAL)
    )

    assert decision.reason == "Runtime health is critical."


def test_wait_does_not_change_runtime_state() -> None:
    runtime = lifecycle()

    recovery = BrainRuntimeRecovery(
        runtime=runtime,
        policy=BrainRuntimeRecoveryPolicy(),
    )

    recovery.apply(
        health(BrainRuntimeHealthLevel.UNKNOWN)
    )

    assert runtime.state is BrainRuntimeLifecycleState.STARTED


def test_policy_reasons_are_stable() -> None:
    policy = BrainRuntimeRecoveryPolicy()

    assert (
        policy.decide(
            health(BrainRuntimeHealthLevel.UNKNOWN)
        ).reason
        == "Runtime health is unknown."
    )
    assert (
        policy.decide(
            health(BrainRuntimeHealthLevel.HEALTHY)
        ).reason
        == "Runtime is healthy."
    )
    assert (
        policy.decide(
            health(BrainRuntimeHealthLevel.DEGRADED)
        ).reason
        == "Runtime is degraded."
    )


def test_critical_recovery_cannot_continue() -> None:
    runtime = lifecycle()

    recovery = BrainRuntimeRecovery(
        runtime=runtime,
        policy=BrainRuntimeRecoveryPolicy(),
    )

    decision = recovery.apply(
        health(BrainRuntimeHealthLevel.CRITICAL)
    )

    assert not decision.can_continue
