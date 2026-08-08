from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_view import BrainViewModel

from .base import Widget


@dataclass(slots=True)
class BrainStatusWidget(Widget):
    view: BrainViewModel | None = None

    def update(
        self,
        view: BrainViewModel,
    ) -> None:
        self.view = view

    @property
    def has_data(self) -> bool:
        return self.view is not None

    @property
    def status(self) -> str:
        if self.view is None:
            return "UNKNOWN"

        return self.view.status

    @property
    def health(self) -> str:
        if self.view is None:
            return "UNKNOWN"

        return self.view.health

    @property
    def cycle(self) -> int | None:
        if self.view is None:
            return None

        return self.view.cycle

    @property
    def execution_percent(self) -> int:
        if self.view is None:
            return 0

        return self.view.execution_percent

    @property
    def target_summary(self) -> str:
        if self.view is None:
            return "0/0 healthy"

        return self.view.target_summary