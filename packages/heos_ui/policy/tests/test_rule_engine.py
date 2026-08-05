
from heos_ui.policy.rules import (
    Rule,
    RuleEngine,
)


def test_enable_disable() -> None:
    engine = RuleEngine()

    engine.add_rule(
        Rule(
            "pv",
            100,
        )
    )

    engine.disable("pv")

    assert engine.enabled_rules() == ()

    engine.enable("pv")

    rules = engine.enabled_rules()

    assert len(rules) == 1
    assert rules[0].enabled