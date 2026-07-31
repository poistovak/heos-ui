from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from .events import StateChangeEvent
from .store import StateStore

StateObserver = Callable[[str, Any], None]
StateEventObserver = Callable[[StateChangeEvent], None]


@dataclass(slots=True)
class ObservableState(StateStore):
    """State store with transactional change notifications."""

    _observers: dict[str, list[StateObserver]] = field(default_factory=dict)
    _event_observers: list[StateEventObserver] = field(default_factory=list)
    _transaction: bool = False
    _pending: dict[str, Any] = field(default_factory=dict)
    _transaction_snapshot: dict[str, Any] | None = None

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

    def subscribe_events(self, observer: StateEventObserver) -> None:
        """Subscribe to all committed state changes."""

        self._event_observers.append(observer)

    def unsubscribe_events(self, observer: StateEventObserver) -> None:
        """Unsubscribe from all state-change events."""

        if observer in self._event_observers:
            self._event_observers.remove(observer)

    def begin(self) -> None:
        self._transaction = True
        self._pending.clear()
        self._transaction_snapshot = dict(self._state)

    def commit(self) -> None:
        if not self._transaction:
            return

        self._transaction = False

        for key, value in self._pending.items():
            self._notify(key, value)

        self._pending.clear()
        self._transaction_snapshot = None

    def rollback(self) -> None:
        if not self._transaction:
            return

        if self._transaction_snapshot is not None:
            self._state.clear()
            self._state.update(self._transaction_snapshot)

        self._transaction = False
        self._pending.clear()
        self._transaction_snapshot = None

    @contextmanager
    def transaction(self) -> Iterator[ObservableState]:
        self.begin()

        try:
            yield self
        except Exception:
            self.rollback()
            raise
        else:
            self.commit()

    def set(self, key: str, value: Any) -> None:
        previous = self.get(key)

        if previous == value:
            return

        super().set(key, value)

        if self._transaction:
            self._pending[key] = value
            return

        self._notify(key, value)

    def update(self, values: Mapping[str, Any]) -> None:
        with self.transaction():
            for key, value in values.items():
                self.set(key, value)

    def snapshot(self) -> dict[str, Any]:
        return dict(self._state)

    def _notify(self, key: str, value: Any) -> None:
        for observer in self._observers.get(key, ()):
            observer(key, value)

        event = StateChangeEvent(key=key, value=value)

        for observer in tuple(self._event_observers):
            observer(event)