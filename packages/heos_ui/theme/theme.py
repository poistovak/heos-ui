from __future__ import annotations

from dataclasses import dataclass

from .colors import (
    ColorPalette,
    ThemeMode,
    get_color_palette,
)
from .spacing import SPACING, SpacingTokens


@dataclass(frozen=True, slots=True)
class HEOSTheme:
    """Complete HEOS UI theme."""

    mode: ThemeMode
    colors: ColorPalette
    spacing: SpacingTokens


def create_theme(mode: ThemeMode | str = ThemeMode.LIGHT) -> HEOSTheme:
    """Create a HEOS UI theme."""

    if not isinstance(mode, ThemeMode):
        mode = ThemeMode(mode)

    return HEOSTheme(
        mode=mode,
        colors=get_color_palette(mode),
        spacing=SPACING,
    )


LIGHT_THEME = create_theme(ThemeMode.LIGHT)

DARK_THEME = create_theme(ThemeMode.DARK)