from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(slots=True)
class Subscription:
    """Handle used to cancel a reactive subscription."""

    _unsubscribe_callback: Callable[[], None]
    _active: bool = field(default=True, init=False)

    @property
    def active(self) -> bool:
        """Return whether the subscription is still active."""

        return self._active

    def unsubscribe(self) -> None:
        """Cancel the subscription.

        Calling this method repeatedly is safe.
        """

        if not self._active:
            return

        self._active = False
        self._unsubscribe_callback()