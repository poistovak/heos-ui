from __future__ import annotations

from dataclasses import dataclass

from heos_ui.theme import LIGHT_THEME, HEOSTheme


@dataclass(frozen=True, slots=True)
class HEOSPanel:
    title: str
    content: str
    theme: HEOSTheme = LIGHT_THEME

    @property
    def background(self) -> str:
        return self.theme.colors.background

    @property
    def foreground(self) -> str:
        return self.theme.colors.text_primary

    @property
    def border(self) -> str:
        return self.theme.colors.border

    @property
    def padding(self) -> int:
        return self.theme.spacing.xl

    def render(self) -> dict[str, object]:
        return {
            "title": self.title,
            "content": self.content,
            "background": self.background,
            "foreground": self.foreground,
            "border": self.border,
            "padding": self.padding,
        }