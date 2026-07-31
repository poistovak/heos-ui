import pytest

from heos_ui.components import HEOSStatus, HEOSStatusLevel
from heos_ui.theme import DARK_THEME, LIGHT_THEME


@pytest.mark.parametrize(
    ("level", "expected_color"),
    [
        (HEOSStatusLevel.INFO, LIGHT_THEME.colors.primary),
        (HEOSStatusLevel.SUCCESS, LIGHT_THEME.colors.success),
        (HEOSStatusLevel.WARNING, LIGHT_THEME.colors.warning),
        (HEOSStatusLevel.ERROR, LIGHT_THEME.colors.danger),
    ],
)
def test_status_colors(level, expected_color):
    status = HEOSStatus(
        text="System status",
        level=level,
    )

    rendered = status.render()

    assert rendered["text"] == "System status"
    assert rendered["level"] == level.value
    assert rendered["color"] == expected_color
    assert rendered["foreground"] == LIGHT_THEME.colors.text_inverse
    assert rendered["padding"] == LIGHT_THEME.spacing.sm


def test_status_dark_theme():
    status = HEOSStatus(
        text="Charging",
        level=HEOSStatusLevel.SUCCESS,
        theme=DARK_THEME,
    )

    rendered = status.render()

    assert rendered["color"] == DARK_THEME.colors.success
    assert rendered["foreground"] == DARK_THEME.colors.text_inverse