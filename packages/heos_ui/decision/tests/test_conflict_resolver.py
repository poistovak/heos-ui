import pytest
from heos_ui.decision import (
    Action,
    ConflictResolver,
    Decision,
    DecisionAction,
)


def candidate(
    *,
    target: str = "wattpilot",
    command: str = "set_current",
    decision_priority: int = 100,
    action_priority: int = 100,
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=decision_priority,
            target=target,
            action=command,
            reason="Policy matched.",
        ),
        action=Action(
            priority=action_priority,
            target=target,
            command=command,
            parameters={},
        ),
    )


def test_empty_candidates() -> None:
    resolver = ConflictResolver()

    assert resolver.resolve([]) == ()


def test_single_candidate_wins() -> None:
    resolver = ConflictResolver()
    item = candidate()

    assert resolver.resolve([item]) == (item,)


def test_higher_decision_priority_wins() -> None:
    resolver = ConflictResolver()

    low = candidate(
        command="set_current",
        decision_priority=10,
    )
    high = candidate(
        command="stop",
        decision_priority=100,
    )

    result = resolver.resolve(
        [
            low,
            high,
        ]
    )

    assert result == (high,)


def test_action_priority_breaks_tie() -> None:
    resolver = ConflictResolver()

    low = candidate(
        command="set_current",
        decision_priority=100,
        action_priority=10,
    )
    high = candidate(
        command="stop",
        decision_priority=100,
        action_priority=200,
    )

    assert resolver.resolve([low, high]) == (high,)


def test_different_targets_are_preserved() -> None:
    resolver = ConflictResolver()

    wattpilot = candidate(
        target="wattpilot",
        decision_priority=100,
    )
    daikin = candidate(
        target="daikin",
        decision_priority=50,
    )

    result = resolver.resolve(
        [
            daikin,
            wattpilot,
        ]
    )

    assert result == (
        wattpilot,
        daikin,
    )


def test_first_candidate_wins_exact_tie() -> None:
    resolver = ConflictResolver()

    first = candidate(command="set_current")
    second = candidate(command="stop")

    assert resolver.resolve([first, second]) == (first,)


def test_target_mismatch_is_rejected() -> None:
    resolver = ConflictResolver()

    invalid = DecisionAction(
        decision=Decision(
            priority=100,
            target="wattpilot",
            action="stop",
            reason="Battery protection.",
        ),
        action=Action(
            priority=100,
            target="daikin",
            command="stop",
        ),
    )

    with pytest.raises(
        ValueError,
        match="target",
    ):
        resolver.resolve([invalid])