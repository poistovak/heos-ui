from __future__ import annotations

from dataclasses import dataclass

from .focus import FocusEngine


@dataclass(slots=True)
class KeyboardNavigator:
    """Keyboard navigation over focused widgets."""

    focus: FocusEngine

    def tab(self) -> str | None:
        return self.focus.next()

    def shift_tab(self) -> str | None:
        return self.focus.previous()

    def home(self) -> str | None:
        widgets = self.focus.registered
        if not widgets:
            return None

        self.focus.focus(widgets[0])
        return self.focus.focused

    def end(self) -> str | None:
        widgets = self.focus.registered
        if not widgets:
            return None

        self.focus.focus(widgets[-1])
        return self.focus.focused