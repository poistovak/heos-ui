from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from heos_ui.decision import Decision


@dataclass(frozen=True, slots=True)
class PolicyRule:
    name: str
    priority: int
    condition: Callable[[dict[str, Any]], bool]
    decision_factory: Callable[[dict[str, Any]], Decision]


@dataclass(slots=True)
class PolicyEngine:
    _rules: list[PolicyRule] = field(
        default_factory=list,
        init=False,
        repr=False,
    )
    _decisions: list[Decision] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def add_rule(self, rule: PolicyRule) -> None:
        self._rules.append(rule)
        self._rules.sort(
            key=lambda item: item.priority,
            reverse=True,
        )

    def evaluate(
        self,
        snapshot: dict[str, Any],
    ) -> tuple[Decision, ...]:
        self._decisions.clear()

        for rule in self._rules:
            if rule.condition(snapshot):
                self._decisions.append(
                    rule.decision_factory(snapshot)
                )

        return self.decisions()

    def decisions(self) -> tuple[Decision, ...]:
        return tuple(self._decisions)

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    def clear(self) -> None:
        self._rules.clear()
        self._decisions.clear()