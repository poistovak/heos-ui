from __future__ import annotations

from dataclasses import dataclass

from heos_ui.theme import LIGHT_THEME, HEOSTheme


@dataclass(frozen=True, slots=True)
class HEOSButton:
    label: str
    enabled: bool = True
    theme: HEOSTheme = LIGHT_THEME

    @property
    def background(self) -> str:
        return (
            self.theme.colors.primary
            if self.enabled
            else self.theme.colors.surface
        )

    @property
    def foreground(self) -> str:
        return self.theme.colors.text_inverse

    @property
    def padding(self) -> int:
        return self.theme.spacing.md

    def render(self) -> dict[str, object]:
        return {
            "label": self.label,
            "enabled": self.enabled,
            "background": self.background,
            "foreground": self.foreground,
            "padding": self.padding,
        }