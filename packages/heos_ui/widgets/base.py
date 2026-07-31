from __future__ import annotations

from dataclasses import dataclass, field

from .lifecycle import WidgetLifecycle


@dataclass(slots=True, kw_only=True)
class Widget:
    """Base class for all HEOS UI widgets."""

    id: str
    title: str
    description: str = ""
    enabled: bool = True
    _lifecycle: WidgetLifecycle = field(
        default=WidgetLifecycle.CREATED,
        init=False,
    )

    @property
    def lifecycle(self) -> WidgetLifecycle:
        """Return the current widget lifecycle state."""

        return self._lifecycle

    @property
    def visible(self) -> bool:
        """Return whether the widget is currently visible."""

        return self._lifecycle is WidgetLifecycle.VISIBLE

    def attach(self) -> None:
        """Attach the widget to a UI container."""

        self._require_state(WidgetLifecycle.CREATED)
        self._lifecycle = WidgetLifecycle.ATTACHED

    def show(self) -> None:
        """Make the widget visible."""

        if not self.enabled:
            raise RuntimeError("Cannot show a disabled widget.")

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

    def enable(self) -> None:
        """Enable the widget."""

        self._require_not_disposed()
        self.enabled = True

    def disable(self) -> None:
        """Disable the widget."""

        self._require_not_disposed()

        if self._lifecycle is WidgetLifecycle.VISIBLE:
            self._lifecycle = WidgetLifecycle.HIDDEN

        self.enabled = False

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

    def _require_not_disposed(self) -> None:
        if self._lifecycle is WidgetLifecycle.DISPOSED:
            raise RuntimeError("Cannot modify a disposed widget.")