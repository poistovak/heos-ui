from heos_ui.layout import (
    Breakpoints,
    ResponsiveLayout,
)


def test_mobile_layout() -> None:
    layout = ResponsiveLayout()

    assert layout.columns(480.0) == 1
    assert layout.spacing(480.0) == 8.0


def test_tablet_layout() -> None:
    layout = ResponsiveLayout()

    assert layout.columns(900.0) == 2
    assert layout.spacing(900.0) == 12.0


def test_desktop_layout() -> None:
    layout = ResponsiveLayout()

    assert layout.columns(1600.0) == 3
    assert layout.spacing(1600.0) == 16.0


def test_breakpoint_edges() -> None:
    layout = ResponsiveLayout()

    assert layout.columns(640.0) == 2
    assert layout.columns(1024.0) == 3


def test_custom_breakpoints() -> None:
    layout = ResponsiveLayout(
        breakpoints=Breakpoints(
            mobile=500.0,
            tablet=900.0,
        )
    )

    assert layout.columns(499.0) == 1
    assert layout.columns(700.0) == 2
    assert layout.columns(1200.0) == 3


def test_spacing_increases_with_width() -> None:
    layout = ResponsiveLayout()

    assert (
        layout.spacing(400.0)
        < layout.spacing(800.0)
        < layout.spacing(1400.0)
    )