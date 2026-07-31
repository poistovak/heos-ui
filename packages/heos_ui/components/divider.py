from __future__ import annotations

from dataclasses import dataclass

from heos_ui.theme import LIGHT_THEME, HEOSTheme


@dataclass(frozen=True, slots=True)
class HEOSDivider:
    thickness: int = 1
    theme: HEOSTheme = LIGHT_THEME

    def __post_init__(self) -> None:
        if self.thickness <= 0:
            raise ValueError("Divider thickness must be greater than zero.")

    @property
    def color(self) -> str:
        return self.theme.colors.border

    @property
    def margin(self) -> int:
        return self.theme.spacing.md

    def render(self) -> dict[str, object]:
        return {
            "color": self.color,
            "thickness": self.thickness,
            "margin": self.margin,
        }