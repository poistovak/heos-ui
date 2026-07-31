from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .store import StateStore

StateObserver = Callable[[str, Any], None]


@dataclass(slots=True)
class ObservableState(StateStore):
    """State store with transactional change notifications."""

    _observers: dict[str, list[StateObserver]] = field(default_factory=dict)
    _transaction: bool = False
    _pending: dict[str, Any] = field(default_factory=dict)

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

    def begin(self) -> None:
        self._transaction = True
        self._pending.clear()

    def commit(self) -> None:
        self._transaction = False

        for key, value in self._pending.items():
            for observer in self._observers.get(key, ()):
                observer(key, value)

        self._pending.clear()

    def set(self, key: str, value: Any) -> None:
        previous = self.get(key)

        if previous == value:
            return

        super().set(key, value)

        if self._transaction:
            self._pending[key] = value
            return

        for observer in self._observers.get(key, ()):
            observer(key, value)

    def update(self, values: Mapping[str, Any]) -> None:
        self.begin()

        for key, value in values.items():
            self.set(key, value)

        self.commit()

    def snapshot(self) -> dict[str, Any]:
        return dict(self._state)