from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StateStore:
    """Central state storage for HEOS UI."""

    _state: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def remove(self, key: str) -> None:
        self._state.pop(key, None)

    def clear(self) -> None:
        self._state.clear()

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def __len__(self) -> int:
        return len(self._state)