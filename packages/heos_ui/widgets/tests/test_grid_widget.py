from heos_ui.widgets.grid import (
    GridState,
    GridWidget,
)


def test_default_state() -> None:
    widget = GridWidget()

    assert widget.power == 0.0
    assert not widget.importing
    assert not widget.exporting
    assert not widget.online


def test_importing() -> None:
    widget = GridWidget()

    widget.update(
        GridState(
            power=3.5,
            importing=True,
            exporting=False,
        )
    )

    assert widget.importing
    assert not widget.exporting
    assert widget.power == 3.5


def test_exporting() -> None:
    widget = GridWidget()

    widget.update(
        GridState(
            power=5.2,
            importing=False,
            exporting=True,
        )
    )

    assert widget.exporting
    assert not widget.importing


def test_replace_state() -> None:
    widget = GridWidget()

    widget.update(GridState(1.0, True, False))
    widget.update(GridState(4.0, False, True))

    assert widget.exporting
    assert widget.power == 4.0


def test_offline() -> None:
    widget = GridWidget()

    widget.update(
        GridState(
            power=0.0,
            importing=False,
            exporting=False,
            online=False,
        )
    )

    assert not widget.online