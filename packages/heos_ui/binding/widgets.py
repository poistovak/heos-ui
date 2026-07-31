from __future__ import annotations

from dataclasses import dataclass

from heos_ui.widgets import ValueWidget

from .binding import StateBinding


@dataclass(slots=True)
class BoundValueWidget(ValueWidget):
    """Value widget backed by a StateBinding."""

    binding: StateBinding

    def refresh(self) -> None:
        value = self.binding.get()

        if not isinstance(value, int | float):
            raise TypeError("Bound value must be numeric.")

        self.value = float(value)