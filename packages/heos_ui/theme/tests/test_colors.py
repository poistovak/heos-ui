from dataclasses import fields

import pytest
from heos_ui.theme.colors import (
    DARK_COLORS,
    LIGHT_COLORS,
    ColorPalette,
    ThemeMode,
    get_color_palette,
)


def test_light_palette_can_be_selected() -> None:
    assert get_color_palette(ThemeMode.LIGHT) is LIGHT_COLORS
    assert get_color_palette("light") is LIGHT_COLORS


def test_dark_palette_can_be_selected() -> None:
    assert get_color_palette(ThemeMode.DARK) is DARK_COLORS
    assert get_color_palette("dark") is DARK_COLORS


def test_unknown_theme_mode_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported theme mode"):
        get_color_palette("midnight")


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("background", "#F4F7FA"),
        ("surface", "#FFFFFF"),
        ("primary", "#1769E0"),
        ("success", "#168A4B"),
        ("energy_solar", "#F4B400"),
        ("energy_battery", "#16A36A"),
    ],
)
def test_light_color_token_can_be_resolved(
    token: str,
    expected: str,
) -> None:
    assert LIGHT_COLORS.resolve(token) == expected


def test_unknown_color_token_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown color token"):
        LIGHT_COLORS.resolve("reactor_glow")


@pytest.mark.parametrize(
    "palette",
    [
        LIGHT_COLORS,
        DARK_COLORS,
    ],
)
def test_all_palette_values_use_hex_notation(
    palette: ColorPalette,
) -> None:
    for field in fields(palette):
        value = getattr(palette, field.name)

        assert value.startswith("#")
        assert len(value) in {7, 9}


def test_light_and_dark_palettes_have_identical_tokens() -> None:
    light_tokens = {field.name for field in fields(LIGHT_COLORS)}
    dark_tokens = {field.name for field in fields(DARK_COLORS)}

    assert light_tokens == dark_tokens


def test_color_palette_is_immutable() -> None:
    with pytest.raises(AttributeError):
        LIGHT_COLORS.primary = "#000000"  # type: ignore[misc]