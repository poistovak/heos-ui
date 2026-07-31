from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ThemeMode(StrEnum):
    """Supported HEOS UI color modes."""

    LIGHT = "light"
    DARK = "dark"


@dataclass(frozen=True, slots=True)
class ColorPalette:
    """Semantic color palette used across the HEOS UI."""

    background: str
    surface: str
    surface_elevated: str

    text_primary: str
    text_secondary: str
    text_disabled: str
    text_inverse: str

    primary: str
    primary_hover: str
    primary_active: str

    secondary: str
    secondary_hover: str

    success: str
    warning: str
    danger: str
    info: str

    border: str
    border_strong: str
    divider: str

    energy_solar: str
    energy_house: str
    energy_grid: str
    energy_battery: str
    energy_ev: str
    energy_heat_pump: str

    overlay: str
    shadow: str

    def resolve(self, token: str) -> str:
        """Resolve a semantic color token to its hexadecimal value."""
        try:
            value = getattr(self, token)
        except AttributeError as exc:
            raise ValueError(f"Unknown color token: {token}") from exc

        if not isinstance(value, str) or not value.startswith("#"):
            raise ValueError(f"Invalid color token: {token}")

        return value


LIGHT_COLORS = ColorPalette(
    background="#F4F7FA",
    surface="#FFFFFF",
    surface_elevated="#FFFFFF",
    text_primary="#15202B",
    text_secondary="#536471",
    text_disabled="#9AA6B2",
    text_inverse="#FFFFFF",
    primary="#1769E0",
    primary_hover="#145CC4",
    primary_active="#104A9F",
    secondary="#5B6472",
    secondary_hover="#484F5A",
    success="#168A4B",
    warning="#D97800",
    danger="#C9363E",
    info="#1677B8",
    border="#D8E0E8",
    border_strong="#B8C4CF",
    divider="#E7ECF1",
    energy_solar="#F4B400",
    energy_house="#1769E0",
    energy_grid="#7B61FF",
    energy_battery="#16A36A",
    energy_ev="#00A6A6",
    energy_heat_pump="#2A8FD4",
    overlay="#66000000",
    shadow="#26000000",
)


DARK_COLORS = ColorPalette(
    background="#0D141C",
    surface="#151F2A",
    surface_elevated="#1B2835",
    text_primary="#F2F6FA",
    text_secondary="#AAB7C4",
    text_disabled="#687786",
    text_inverse="#101820",
    primary="#5A9BFF",
    primary_hover="#76ACFF",
    primary_active="#3E87F5",
    secondary="#A7B1BC",
    secondary_hover="#C1C9D1",
    success="#43C980",
    warning="#FFB84D",
    danger="#FF6670",
    info="#55B8F2",
    border="#2D3B49",
    border_strong="#425364",
    divider="#24313E",
    energy_solar="#FFD34E",
    energy_house="#5A9BFF",
    energy_grid="#A58BFF",
    energy_battery="#43C980",
    energy_ev="#45D3D3",
    energy_heat_pump="#55B8F2",
    overlay="#99000000",
    shadow="#80000000",
)


def get_color_palette(mode: ThemeMode | str) -> ColorPalette:
    """Return the color palette for the requested theme mode."""
    try:
        resolved_mode = ThemeMode(mode)
    except ValueError as exc:
        raise ValueError(f"Unsupported theme mode: {mode}") from exc

    if resolved_mode is ThemeMode.LIGHT:
        return LIGHT_COLORS

    return DARK_COLORS