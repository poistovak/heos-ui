from __future__ import annotations

from heos_ui.widgets.base import Widget


class FrameBatch:
    """Separates the current render frame from the next frame."""

    def __init__(self) -> None:
        self._pending: dict[int, Widget] = {}
        self._current: tuple[Widget, ...] = ()
        self._active = False
        self._frame_id = 0

    @property
    def frame_id(self) -> int:
        return self._frame_id

    @property
    def active(self) -> bool:
        return self._active

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    @property
    def current_widgets(self) -> tuple[Widget, ...]:
        return self._current

    def enqueue(self, widget: Widget) -> None:
        """Schedule a widget for the next available frame."""

        self._pending.setdefault(id(widget), widget)

    def begin(self) -> tuple[Widget, ...]:
        """Freeze pending widgets as the current frame."""

        if self._active:
            raise RuntimeError("A render frame is already active.")

        self._current = tuple(self._pending.values())
        self._pending.clear()
        self._active = True
        self._frame_id += 1
        return self._current

    def end(self) -> None:
        """Finish the active frame."""

        if not self._active:
            raise RuntimeError("No render frame is active.")

        self._current = ()
        self._active = False

    def clear(self) -> None:
        """Discard widgets waiting for a future frame."""

        self._pending.clear()
