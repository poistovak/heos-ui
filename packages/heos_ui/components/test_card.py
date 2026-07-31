from heos_ui.components import HEOSCard
from heos_ui.theme import DARK_THEME, LIGHT_THEME


def test_card_defaults():
    card = HEOSCard(
        title="Solar",
        content="8.4 kW",
    )

    rendered = card.render()

    assert rendered["title"] == "Solar"
    assert rendered["content"] == "8.4 kW"
    assert rendered["background"] == LIGHT_THEME.colors.surface
    assert rendered["border"] == LIGHT_THEME.colors.border
    assert rendered["padding"] == LIGHT_THEME.spacing.lg


def test_card_dark_theme():
    card = HEOSCard(
        title="Battery",
        content="82 %",
        theme=DARK_THEME,
    )

    rendered = card.render()

    assert rendered["background"] == DARK_THEME.colors.surface
    assert rendered["border"] == DARK_THEME.colors.border