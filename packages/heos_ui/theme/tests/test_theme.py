import pytest
from heos_ui.theme.colors import ThemeMode
from heos_ui.theme.spacing import SPACING
from heos_ui.theme.theme import (
    DARK_THEME,
    LIGHT_THEME,
    HEOSTheme,
    create_theme,
)


def test_create_light_theme() -> None:
    theme = create_theme()

    assert isinstance(theme, HEOSTheme)
    assert theme.mode is ThemeMode.LIGHT
    assert theme.spacing is SPACING


def test_create_dark_theme() -> None:
    theme = create_theme(ThemeMode.DARK)

    assert theme.mode is ThemeMode.DARK


@pytest.mark.parametrize(
    "mode",
    [
        ThemeMode.LIGHT,
        ThemeMode.DARK,
        "light",
        "dark",
    ],
)
def test_create_theme_accepts_supported_modes(mode) -> None:
    assert create_theme(mode)


def test_invalid_mode() -> None:
    with pytest.raises(ValueError):
        create_theme("blue")


def test_singletons() -> None:
    assert LIGHT_THEME.mode is ThemeMode.LIGHT
    assert DARK_THEME.mode is ThemeMode.DARK


def test_spacing_is_shared() -> None:
    assert LIGHT_THEME.spacing is DARK_THEME.spacing