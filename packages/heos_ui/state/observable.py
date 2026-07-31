from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .store import StateStore

StateObserver = Callable[[str, Any], None]


@dataclass(slots=True)
class ObservableState(StateStore):
    """State store with key-filtered change notifications."""

    _observers: dict[str, list[StateObserver]] = field(default_factory=dict)

    def subscribe(self, key: str, observer: StateObserver) -> None:
        self._observers.setdefault(key, []).append(observer)

    def unsubscribe(self, key: str, observer: StateObserver) -> None:
        observers = self._observers.get(key)
        if observers is None:
            return

        if observer in observers:
            observers.remove(observer)

        if not observers:
            self._observers.pop(key, None)

    def set(self, key: str, value: Any) -> None:
        previous = self.get(key)

        if previous == value:
            return

        super().set(key, value)

        for observer in self._observers.get(key, ()):
            observer(key, value)

    def update(self, values: Mapping[str, Any]) -> None:
        """Update multiple state values."""

        for key, value in values.items():
            self.set(key, value)

    def snapshot(self) -> dict[str, Any]:
        """Return an independent copy of the current state."""

        return dict(self._state)