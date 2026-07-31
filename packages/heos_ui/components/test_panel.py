from heos_ui.components import HEOSPanel
from heos_ui.theme import DARK_THEME, LIGHT_THEME


def test_panel_defaults():
    panel = HEOSPanel(
        title="Energy Overview",
        content="System nominal",
    )

    rendered = panel.render()

    assert rendered["title"] == "Energy Overview"
    assert rendered["content"] == "System nominal"
    assert rendered["background"] == LIGHT_THEME.colors.background
    assert rendered["foreground"] == LIGHT_THEME.colors.text_primary
    assert rendered["border"] == LIGHT_THEME.colors.border
    assert rendered["padding"] == LIGHT_THEME.spacing.xl


def test_panel_dark_theme():
    panel = HEOSPanel(
        title="Battery",
        content="Charging",
        theme=DARK_THEME,
    )

    rendered = panel.render()

    assert rendered["background"] == DARK_THEME.colors.background
    assert rendered["foreground"] == DARK_THEME.colors.text_primary
    assert rendered["border"] == DARK_THEME.colors.border