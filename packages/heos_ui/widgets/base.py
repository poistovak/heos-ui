from __future__ import annotations

from dataclasses import dataclass, field

from .lifecycle import WidgetLifecycle


@dataclass(slots=True)
class Widget:
    """Base class for all HEOS UI widgets."""

    id: str
    title: str
    _lifecycle: WidgetLifecycle = field(
        default=WidgetLifecycle.CREATED,
        init=False,
    )

    @property
    def lifecycle(self) -> WidgetLifecycle:
        """Return the current widget lifecycle state."""

        return self._lifecycle

    def attach(self) -> None:
        """Attach the widget to a UI container."""

        self._require_state(WidgetLifecycle.CREATED)
        self._lifecycle = WidgetLifecycle.ATTACHED

    def show(self) -> None:
        """Make the widget visible."""

        if self._lifecycle not in {
            WidgetLifecycle.ATTACHED,
            WidgetLifecycle.HIDDEN,
        }:
            raise RuntimeError(
                f"Cannot show widget in state {self._lifecycle.value}."
            )

        self._lifecycle = WidgetLifecycle.VISIBLE

    def hide(self) -> None:
        """Hide a visible widget."""

        self._require_state(WidgetLifecycle.VISIBLE)
        self._lifecycle = WidgetLifecycle.HIDDEN

    def dispose(self) -> None:
        """Dispose the widget and release its lifecycle."""

        if self._lifecycle is WidgetLifecycle.DISPOSED:
            return

        self._lifecycle = WidgetLifecycle.DISPOSED

    def render(self) -> str:
        """Return a text representation of the widget."""

        return self.title

    def _require_state(self, expected: WidgetLifecycle) -> None:
        if self._lifecycle is not expected:
            raise RuntimeError(
                f"Expected widget state {expected.value}, "
                f"got {self._lifecycle.value}."
            )