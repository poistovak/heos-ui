from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from heos_ui.decision import Action


@dataclass(slots=True)
class AdapterDispatcher:
    _adapters: dict[str, Callable[[Action], Any]] = field(
        default_factory=dict,
        init=False,
    )

    def register(
        self,
        target: str,
        adapter: Callable[[Action], Any],
    ) -> None:
        self._adapters[target] = adapter

    def dispatch(
        self,
        action: Action,
    ) -> Any:
        adapter = self._adapters.get(action.target)

        if adapter is None:
            raise KeyError(
                f"No adapter registered for '{action.target}'."
            )

        return adapter(action)

    def has_adapter(
        self,
        target: str,
    ) -> bool:
        return target in self._adapters

    @property
    def adapter_count(self) -> int:
        return len(self._adapters)

    def clear(self) -> None:
        self._adapters.clear()