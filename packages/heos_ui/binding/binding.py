from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from heos_ui.state import StateStore


@dataclass(slots=True)
class StateBinding:
    """Binds one state key to a UI value."""

    store: StateStore
    key: str
    default: Any = None

    def get(self) -> Any:
        return self.store.get(self.key, self.default)