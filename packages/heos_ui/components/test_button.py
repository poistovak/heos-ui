from heos_ui.components import HEOSButton
from heos_ui.theme import DARK_THEME, LIGHT_THEME


def test_button_enabled():
    button = HEOSButton("Start")

    rendered = button.render()

    assert rendered["label"] == "Start"
    assert rendered["enabled"] is True
    assert rendered["background"] == LIGHT_THEME.colors.primary
    assert rendered["foreground"] == LIGHT_THEME.colors.text_inverse
    assert rendered["padding"] == LIGHT_THEME.spacing.md


def test_button_disabled():
    button = HEOSButton(
        "Stop",
        enabled=False,
        theme=DARK_THEME,
    )

    rendered = button.render()

    assert rendered["enabled"] is False
    assert rendered["background"] == DARK_THEME.colors.surface