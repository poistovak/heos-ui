from heos_ui.theme import DEFAULT_THEME, Theme


def test_default_theme() -> None:
    assert isinstance(DEFAULT_THEME, Theme)
    assert DEFAULT_THEME.name == "HEOS Dark"
    assert DEFAULT_THEME.primary == "#2D81FF"
    assert DEFAULT_THEME.secondary == "#9AA4B2"
    assert DEFAULT_THEME.success == "#4CAF50"
    assert DEFAULT_THEME.warning == "#FFC107"
    assert DEFAULT_THEME.danger == "#F44336"