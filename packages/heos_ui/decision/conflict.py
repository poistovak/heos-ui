from __future__ import annotations

from dataclasses import dataclass

from .action_queue import Action
from .planner import Decision


@dataclass(frozen=True, slots=True)
class DecisionAction:
    decision: Decision
    action: Action


class ConflictResolver:
    """Resolve competing decisions for the same target."""

    def resolve(
        self,
        candidates: list[DecisionAction],
    ) -> tuple[DecisionAction, ...]:
        winners: dict[str, DecisionAction] = {}

        for candidate in candidates:
            self._validate(candidate)

            current = winners.get(candidate.action.target)

            if current is None:
                winners[candidate.action.target] = candidate
                continue

            if candidate.decision.priority > current.decision.priority:
                winners[candidate.action.target] = candidate
                continue

            if (
                candidate.decision.priority == current.decision.priority
                and candidate.action.priority > current.action.priority
            ):
                winners[candidate.action.target] = candidate

        return tuple(
            sorted(
                winners.values(),
                key=lambda item: (
                    item.decision.priority,
                    item.action.priority,
                ),
                reverse=True,
            )
        )

    def _validate(
        self,
        candidate: DecisionAction,
    ) -> None:
        if candidate.decision.target != candidate.action.target:
            raise ValueError(
                "Decision target and action target must match."
            )