from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from heos_ui.decision import Action


@dataclass(slots=True)
class ExecutionEngine:
    _handlers: dict[str, Callable[[Action], Any]] = field(
        default_factory=dict,
        init=False,
    )

    def register(
        self,
        target: str,
        handler: Callable[[Action], Any],
    ) -> None:
        self._handlers[target] = handler

    def execute(
        self,
        action: Action,
    ) -> Any:
        handler = self._handlers.get(action.target)

        if handler is None:
            raise KeyError(
                f"No handler registered for '{action.target}'."
            )

        return handler(action)

    def has_handler(
        self,
        target: str,
    ) -> bool:
        return target in self._handlers

    @property
    def handler_count(self) -> int:
        return len(self._handlers)

    def clear(self) -> None:
        self._handlers.clear()