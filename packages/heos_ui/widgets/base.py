from __future__ import annotations

from dataclasses import dataclass, field

from .lifecycle import WidgetLifecycle


@dataclass(slots=True)
class Widget:
    """Base class for all HEOS UI widgets."""

    id: str
    title: str
    description: str = field(default="", kw_only=True)
    _lifecycle: WidgetLifecycle = field(
        default=WidgetLifecycle.CREATED,
        init=False,
    )
    _enabled: bool = field(
        default=True,
        init=False,
    )
    _dirty: bool = field(
        default=False,
        init=False,
    )
    _render_count: int = field(
        default=0,
        init=False,
    )

    @property
    def lifecycle(self) -> WidgetLifecycle:
        """Return the current widget lifecycle state."""

        return self._lifecycle

    @property
    def enabled(self) -> bool:
        """Return whether the widget is enabled."""

        return self._enabled

    @property
    def visible(self) -> bool:
        """Return whether the widget is currently visible."""

        return self._lifecycle is WidgetLifecycle.VISIBLE

    @property
    def dirty(self) -> bool:
        """Return whether the widget requires rendering."""

        return self._dirty

    @property
    def render_count(self) -> int:
        """Return the number of completed renders."""

        return self._render_count

    def attach(self) -> None:
        """Attach the widget to a UI container."""

        self._require_state(WidgetLifecycle.CREATED)
        self._lifecycle = WidgetLifecycle.ATTACHED

    def show(self) -> None:
        """Make the widget visible."""

        if not self._enabled:
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
        """Hide the widget."""

        self._require_state(WidgetLifecycle.VISIBLE)
        self._lifecycle = WidgetLifecycle.HIDDEN

    def enable(self) -> None:
        """Enable the widget."""

        if self._lifecycle is WidgetLifecycle.DISPOSED:
            raise RuntimeError("Cannot modify a disposed widget.")

        self._enabled = True

    def disable(self) -> None:
        """Disable the widget and hide it when currently visible."""

        if self._lifecycle is WidgetLifecycle.DISPOSED:
            return

        self._enabled = False

        if self._lifecycle is WidgetLifecycle.VISIBLE:
            self._lifecycle = WidgetLifecycle.HIDDEN

    def detach(self) -> None:
        """Detach the widget from its UI container."""

        if self._lifecycle not in {
            WidgetLifecycle.ATTACHED,
            WidgetLifecycle.VISIBLE,
            WidgetLifecycle.HIDDEN,
        }:
            raise RuntimeError(
                f"Cannot detach widget in state {self._lifecycle.value}."
            )

        self._lifecycle = WidgetLifecycle.DETACHED

    def dispose(self) -> None:
        """Dispose the widget.

        Calling this method repeatedly is safe.
        """

        if self._lifecycle is WidgetLifecycle.DISPOSED:
            return

        self._enabled = False
        self._dirty = False
        self._lifecycle = WidgetLifecycle.DISPOSED

    def invalidate(self) -> bool:
        """Mark the widget as requiring rendering.

        Returns:
            True when the widget became dirty, otherwise False.
        """

        if self._lifecycle is WidgetLifecycle.DISPOSED:
            return False

        if self._dirty:
            return False

        self._dirty = True
        return True

    def render_if_dirty(self) -> bool:
        """Render the widget only when it is dirty.

        Returns:
            True when rendering occurred, otherwise False.
        """

        if not self._dirty:
            return False

        if self._lifecycle is WidgetLifecycle.DISPOSED:
            self._dirty = False
            return False

        self.render()
        self._dirty = False
        self._render_count += 1
        return True

    def render(self) -> None:
        """Render the widget.

        Concrete widget implementations may override this method.
        """

    def _require_state(self, expected: WidgetLifecycle) -> None:
        if self._lifecycle is not expected:
            raise RuntimeError(
                f"Expected widget state {expected.value}, "
                f"got {self._lifecycle.value}."
            )