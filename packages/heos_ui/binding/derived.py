from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from heos_ui.state import ComputedState


@dataclass(slots=True)
class DerivedBinding:
    """Binds a widget to a computed state."""

    computed: ComputedState

    def value(self) -> Any:
        return self.computed.value()