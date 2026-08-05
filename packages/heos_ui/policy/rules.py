from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.energy import EnergySnapshot


@dataclass(frozen=True, slots=True)
class Rule:
    name: str
    priority: int
    enabled: bool = True


@dataclass(slots=True)
class RuleEngine:
    _rules: dict[str, Rule] = field(
        default_factory=dict,
        init=False,
    )

    def add_rule(
        self,
        rule: Rule,
    ) -> None:
        if rule.name in self._rules:
            raise ValueError(
                f"Rule '{rule.name}' already exists."
            )

        self._rules[rule.name] = rule

    def remove_rule(
        self,
        name: str,
    ) -> None:
        self._rules.pop(name)

    def enable(
        self,
        name: str,
    ) -> None:
        rule = self._rules[name]
        self._rules[name] = Rule(
            name=rule.name,
            priority=rule.priority,
            enabled=True,
        )

    def disable(
        self,
        name: str,
    ) -> None:
        rule = self._rules[name]
        self._rules[name] = Rule(
            name=rule.name,
            priority=rule.priority,
            enabled=False,
        )

    def enabled_rules(self) -> tuple[Rule, ...]:
        return tuple(
            sorted(
                (
                    rule
                    for rule in self._rules.values()
                    if rule.enabled
                ),
                key=lambda item: item.priority,
                reverse=True,
            )
        )

    def evaluate(
        self,
        snapshot: EnergySnapshot,
    ) -> tuple[Rule, ...]:
        return self.enabled_rules()

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    def clear(self) -> None:
        self._rules.clear()