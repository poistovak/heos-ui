from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from heos_ui.decision import Action, Decision
from heos_ui.energy import EnergySnapshot


class Scenario(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def priority(self) -> int: ...

    @property
    def enabled(self) -> bool: ...

    def evaluate(
        self,
        snapshot: EnergySnapshot,
    ) -> tuple[Decision | None, Action | None]: ...


@dataclass(slots=True)
class ScenarioManager:
    _scenarios: list[Scenario] = field(
        default_factory=list,
        init=False,
    )

    def register(
        self,
        scenario: Scenario,
    ) -> None:
        self._scenarios.append(scenario)
        self._scenarios.sort(
            key=lambda s: s.priority,
            reverse=True,
        )

    def evaluate(
        self,
        snapshot: EnergySnapshot,
    ) -> list[tuple[Decision, Action]]:
        result: list[tuple[Decision, Action]] = []

        for scenario in self._scenarios:
            if not scenario.enabled:
                continue

            decision, action = scenario.evaluate(snapshot)

            if decision and action:
                result.append(
                    (
                        decision,
                        action,
                    )
                )

        return result

    @property
    def count(self) -> int:
        return len(self._scenarios)

    def clear(self) -> None:
        self._scenarios.clear()