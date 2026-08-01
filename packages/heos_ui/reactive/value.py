from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

from .subscription import Subscription

T = TypeVar("T")

Subscriber = Callable[[T], None]


class ReactiveValue(Generic[T]):
    """Observable value that notifies subscribers after a real change."""

    def __init__(self, value: T) -> None:
        self._value = value
        self._subscribers: list[Subscriber[T]] = []

    @property
    def value(self) -> T:
        """Return the current value."""

        return self._value

    def get(self) -> T:
        """Return the current value."""

        return self._value

    def set(self, value: T) -> bool:
        """Set a new value and notify subscribers when it changed.

        Returns:
            True when the value changed, otherwise False.
        """

        if value == self._value:
            return False

        self._value = value

        for subscriber in tuple(self._subscribers):
            if subscriber in self._subscribers:
                subscriber(value)

        return True

    def subscribe(
        self,
        subscriber: Subscriber[T],
        *,
        notify_immediately: bool = False,
    ) -> Subscription:
        """Subscribe to value changes."""

        self._subscribers.append(subscriber)

        if notify_immediately:
            subscriber(self._value)

        def unsubscribe() -> None:
            try:
                self._subscribers.remove(subscriber)
            except ValueError:
                pass

        return Subscription(unsubscribe)

    @property
    def subscriber_count(self) -> int:
        """Return the number of active subscribers."""

        return len(self._subscribers)