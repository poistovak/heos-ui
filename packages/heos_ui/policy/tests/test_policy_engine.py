from heos_ui.decision import Decision
from heos_ui.policy import PolicyEngine, PolicyRule


def decision(
    target: str,
    priority: int,
) -> Decision:
    return Decision(
        priority=priority,
        target=target,
        action="set_current",
        reason="Policy matched.",
    )


def test_starts_empty() -> None:
    engine = PolicyEngine()

    assert engine.rule_count == 0
    assert engine.decisions() == ()


def test_add_rule() -> None:
    engine = PolicyEngine()

    engine.add_rule(
        PolicyRule(
            name="surplus",
            priority=100,
            condition=lambda snapshot: True,
            decision_factory=lambda snapshot: decision(
                "wattpilot",
                100,
            ),
        )
    )

    assert engine.rule_count == 1


def test_evaluate_matching_rule() -> None:
    engine = PolicyEngine()

    engine.add_rule(
        PolicyRule(
            name="surplus",
            priority=100,
            condition=lambda snapshot: snapshot["surplus"] > 2500,
            decision_factory=lambda snapshot: decision(
                "wattpilot",
                100,
            ),
        )
    )

    decisions = engine.evaluate(
        {"surplus": 3000}
    )

    assert len(decisions) == 1
    assert decisions[0].target == "wattpilot"


def test_no_match() -> None:
    engine = PolicyEngine()

    engine.add_rule(
        PolicyRule(
            name="surplus",
            priority=100,
            condition=lambda snapshot: snapshot["surplus"] > 2500,
            decision_factory=lambda snapshot: decision(
                "wattpilot",
                100,
            ),
        )
    )

    assert engine.evaluate(
        {"surplus": 1000}
    ) == ()


def test_multiple_rules_follow_priority() -> None:
    engine = PolicyEngine()

    engine.add_rule(
        PolicyRule(
            name="low",
            priority=10,
            condition=lambda snapshot: True,
            decision_factory=lambda snapshot: decision(
                "daikin",
                10,
            ),
        )
    )
    engine.add_rule(
        PolicyRule(
            name="high",
            priority=100,
            condition=lambda snapshot: True,
            decision_factory=lambda snapshot: decision(
                "wattpilot",
                100,
            ),
        )
    )

    decisions = engine.evaluate({})

    assert tuple(
        item.target for item in decisions
    ) == (
        "wattpilot",
        "daikin",
    )


def test_clear() -> None:
    engine = PolicyEngine()

    engine.add_rule(
        PolicyRule(
            name="rule",
            priority=1,
            condition=lambda snapshot: True,
            decision_factory=lambda snapshot: decision(
                "wattpilot",
                1,
            ),
        )
    )

    engine.evaluate({})
    engine.clear()

    assert engine.rule_count == 0
    assert engine.decisions() == ()