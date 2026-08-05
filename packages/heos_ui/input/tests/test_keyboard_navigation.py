from heos_ui.input.focus import FocusEngine
from heos_ui.input.keyboard import KeyboardNavigator


def create() -> KeyboardNavigator:
    focus = FocusEngine()

    focus.register("solar")
    focus.register("battery")
    focus.register("car")

    return KeyboardNavigator(focus)


def test_tab() -> None:
    nav = create()

    assert nav.tab() == "battery"


def test_shift_tab() -> None:
    nav = create()

    assert nav.shift_tab() == "car"


def test_home() -> None:
    nav = create()

    nav.tab()
    nav.tab()

    assert nav.home() == "solar"


def test_end() -> None:
    nav = create()

    assert nav.end() == "car"


def test_tab_wraps() -> None:
    nav = create()

    nav.tab()
    nav.tab()

    assert nav.tab() == "solar"


def test_shift_wraps() -> None:
    nav = create()

    assert nav.shift_tab() == "car"


def test_empty_navigation() -> None:
    nav = KeyboardNavigator(FocusEngine())

    assert nav.tab() is None
    assert nav.shift_tab() is None
    assert nav.home() is None
    assert nav.end() is None