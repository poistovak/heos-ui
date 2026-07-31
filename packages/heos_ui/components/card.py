from __future__ import annotations

from dataclasses import dataclass

from heos_ui.theme import LIGHT_THEME, HEOSTheme


@dataclass(frozen=True, slots=True)
class HEOSCard:
    title: str
    content: str
    theme: HEOSTheme = LIGHT_THEME

    @property
    def background(self) -> str:
        return self.theme.colors.surface

    @property
    def border(self) -> str:
        return self.theme.colors.border

    @property
    def padding(self) -> int:
        return self.theme.spacing.lg

    def render(self) -> dict[str, object]:
        return {
            "title": self.title,
            "content": self.content,
            "background": self.background,
            "border": self.border,
            "padding": self.padding,
        }