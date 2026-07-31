from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .observable import ObservableState


@dataclass(slots=True)
class ComputedState:
    """Represents a computed value derived from ObservableState."""

    state: ObservableState
    computer: Callable[[ObservableState], Any]

    def value(self) -> Any:
        return self.computer(self.state)