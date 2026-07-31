from heos_ui.components import HEOSProgress
from heos_ui.theme import LIGHT_THEME


def test_progress_half():
    progress = HEOSProgress(50)

    rendered = progress.render()

    assert rendered["percentage"] == 50.0
    assert rendered["fill_color"] == LIGHT_THEME.colors.primary
    assert rendered["track_color"] == LIGHT_THEME.colors.surface


def test_progress_clamped():
    progress = HEOSProgress(250)

    assert progress.percentage == 100.0


def test_progress_zero():
    progress = HEOSProgress(-20)

    assert progress.percentage == 0.0