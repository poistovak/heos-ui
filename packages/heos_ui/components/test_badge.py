from heos_ui.components import HEOSBadge
from heos_ui.theme import LIGHT_THEME


def test_badge_render():
    badge = HEOSBadge("ONLINE")

    rendered = badge.render()

    assert rendered["text"] == "ONLINE"
    assert rendered["background"] == LIGHT_THEME.colors.primary
    assert rendered["foreground"] == LIGHT_THEME.colors.text_inverse
    assert rendered["padding"] == LIGHT_THEME.spacing.sm