from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from heos_ui.theme import LIGHT_THEME, HEOSTheme


class HEOSStatusLevel(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class HEOSStatus:
    text: str
    level: HEOSStatusLevel = HEOSStatusLevel.INFO
    theme: HEOSTheme = LIGHT_THEME

    @property
    def color(self) -> str:
        colors = self.theme.colors

        return {
            HEOSStatusLevel.INFO: colors.primary,
            HEOSStatusLevel.SUCCESS: colors.success,
            HEOSStatusLevel.WARNING: colors.warning,
            HEOSStatusLevel.ERROR: colors.danger,
        }[self.level]

    @property
    def foreground(self) -> str:
        return self.theme.colors.text_inverse

    @property
    def padding(self) -> int:
        return self.theme.spacing.sm

    def render(self) -> dict[str, object]:
        return {
            "text": self.text,
            "level": self.level.value,
            "color": self.color,
            "foreground": self.foreground,
            "padding": self.padding,
        }