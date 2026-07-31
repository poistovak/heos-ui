import pytest

from heos_ui.components import HEOSDivider
from heos_ui.theme import DARK_THEME, LIGHT_THEME


def test_divider_defaults():
    divider = HEOSDivider()

    rendered = divider.render()

    assert rendered["color"] == LIGHT_THEME.colors.border
    assert rendered["thickness"] == 1
    assert rendered["margin"] == LIGHT_THEME.spacing.md


def test_divider_dark_theme():
    divider = HEOSDivider(
        thickness=2,
        theme=DARK_THEME,
    )

    rendered = divider.render()

    assert rendered["color"] == DARK_THEME.colors.border
    assert rendered["thickness"] == 2


def test_divider_rejects_invalid_thickness():
    with pytest.raises(
        ValueError,
        match="Divider thickness must be greater than zero.",
    ):
        HEOSDivider(thickness=0)