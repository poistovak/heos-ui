from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FocusEngine:
    """Tracks focus across registered widgets."""

    _widgets: list[str] = field(
        default_factory=list,
        init=False,
        repr=False,
    )
    _focused_index: int | None = field(
        default=None,
        init=False,
        repr=False,
    )

    @property
    def focused(self) -> str | None:
        if self._focused_index is None:
            return None

        return self._widgets[self._focused_index]

    @property
    def registered(self) -> tuple[str, ...]:
        return tuple(self._widgets)

    def register(self, widget_id: str) -> None:
        if widget_id in self._widgets:
            return

        self._widgets.append(widget_id)

        if self._focused_index is None:
            self._focused_index = 0

    def unregister(self, widget_id: str) -> None:
        if widget_id not in self._widgets:
            return

        index = self._widgets.index(widget_id)
        self._widgets.remove(widget_id)

        if not self._widgets:
            self._focused_index = None
            return

        if self._focused_index is None:
            self._focused_index = 0
            return

        if index < self._focused_index:
            self._focused_index -= 1
        elif index == self._focused_index:
            self._focused_index = min(
                self._focused_index,
                len(self._widgets) - 1,
            )

    def focus(self, widget_id: str) -> bool:
        if widget_id not in self._widgets:
            return False

        self._focused_index = self._widgets.index(widget_id)
        return True

    def next(self) -> str | None:
        if not self._widgets:
            return None

        if self._focused_index is None:
            self._focused_index = 0
        else:
            self._focused_index = (
                self._focused_index + 1
            ) % len(self._widgets)

        return self.focused

    def previous(self) -> str | None:
        if not self._widgets:
            return None

        if self._focused_index is None:
            self._focused_index = 0
        else:
            self._focused_index = (
                self._focused_index - 1
            ) % len(self._widgets)

        return self.focused

    def clear(self) -> None:
        self._focused_index = None