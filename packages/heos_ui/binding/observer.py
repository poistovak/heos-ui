from __future__ import annotations

from dataclasses import dataclass

from heos_ui.state import ObservableState

from .widgets import BoundValueWidget


@dataclass(slots=True)
class WidgetObserver:
    """Refreshes a bound widget when its state key changes."""

    state: ObservableState
    key: str
    widget: BoundValueWidget

    def __post_init__(self) -> None:
        self.state.subscribe(self.key, self._on_state_changed)

    def _on_state_changed(self, key: str, value: object) -> None:
        self.widget.refresh()

    def dispose(self) -> None:
        self.state.unsubscribe(self.key, self._on_state_changed)