import pytest

from heos_ui.adapters import AdapterDispatcher
from heos_ui.decision import (
    Action,
    ActionQueue,
    Decision,
    DecisionPlanner,
)
from heos_ui.energy.control_loop import EnergyControlLoop
from heos_ui.execution import ExecutionEngine


def create_loop() -> EnergyControlLoop:
    return EnergyControlLoop(
        planner=DecisionPlanner(),
        actions=ActionQueue(),
        execution=ExecutionEngine(),
        dispatcher=AdapterDispatcher(),
    )


def decision(
    target: str = "wattpilot",
    priority: int = 100,
) -> Decision:
    return Decision(
        priority=priority,
        target=target,
        action="set_current",
        reason="PV surplus available.",
    )


def action(
    target: str = "wattpilot",
    priority: int = 100,
) -> Action:
    return Action(
        priority=priority,
        target=target,
        command="set_current",
        parameters={"amps": 16},
    )


def test_starts_empty() -> None:
    loop = create_loop()

    assert loop.pending == 0


def test_submit() -> None:
    loop = create_loop()

    loop.submit(
        decision(),
        action(),
    )

    assert loop.pending == 1


def test_run_once_executes_action() -> None:
    loop = create_loop()

    loop.dispatcher.register(
        "wattpilot",
        lambda item: item.parameters["amps"],
    )
    loop.submit(
        decision(),
        action(),
    )

    result = loop.run_once()

    assert result.executed
    assert result.result == 16
    assert loop.pending == 0


def test_empty_loop_does_not_execute() -> None:
    loop = create_loop()

    result = loop.run_once()

    assert not result.executed
    assert result.decision is None
    assert result.action is None


def test_target_mismatch_is_rejected() -> None:
    loop = create_loop()

    loop.submit(
        decision("wattpilot"),
        action("daikin"),
    )

    with pytest.raises(
        ValueError,
        match="target",
    ):
        loop.run_once()


def test_priority_ordering() -> None:
    loop = create_loop()
    executed = []

    loop.dispatcher.register(
        "wattpilot",
        lambda item: executed.append(
            item.parameters["amps"]
        ),
    )

    loop.submit(
        decision(priority=10),
        Action(
            priority=10,
            target="wattpilot",
            command="set_current",
            parameters={"amps": 6},
        ),
    )
    loop.submit(
        decision(priority=100),
        Action(
            priority=100,
            target="wattpilot",
            command="set_current",
            parameters={"amps": 16},
        ),
    )

    loop.run_once()
    loop.run_once()

    assert executed == [16, 6]


def test_clear() -> None:
    loop = create_loop()

    loop.submit(
        decision(),
        action(),
    )
    loop.clear()

    assert loop.pending == 0