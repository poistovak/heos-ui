from __future__ import annotations

from dataclasses import dataclass

from heos_ui.theme import LIGHT_THEME, HEOSTheme


@dataclass(frozen=True, slots=True)
class HEOSProgress:
    value: float
    minimum: float = 0.0
    maximum: float = 100.0
    theme: HEOSTheme = LIGHT_THEME

    @property
    def percentage(self) -> float:
        if self.maximum <= self.minimum:
            return 0.0

        value = min(max(self.value, self.minimum), self.maximum)

        return (
            (value - self.minimum)
            / (self.maximum - self.minimum)
        ) * 100.0

    @property
    def track_color(self) -> str:
        return self.theme.colors.surface

    @property
    def fill_color(self) -> str:
        return self.theme.colors.primary

    @property
    def height(self) -> int:
        return self.theme.spacing.sm

    def render(self) -> dict[str, object]:
        return {
            "value": self.value,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "percentage": round(self.percentage, 1),
            "track_color": self.track_color,
            "fill_color": self.fill_color,
            "height": self.height,
        }