from __future__ import annotations

from dataclasses import dataclass

from heos_ui.theme import LIGHT_THEME, HEOSTheme


@dataclass(frozen=True, slots=True)
class HEOSBadge:
    text: str
    theme: HEOSTheme = LIGHT_THEME

    @property
    def background(self) -> str:
        return self.theme.colors.primary

    @property
    def foreground(self) -> str:
        return self.theme.colors.text_inverse

    @property
    def padding(self) -> int:
        return self.theme.spacing.sm

    def render(self) -> dict[str, object]:
        return {
            "text": self.text,
            "background": self.background,
            "foreground": self.foreground,
            "padding": self.padding,
        }