from heos_ui.input.focus import FocusEngine


def test_starts_empty() -> None:
    engine = FocusEngine()

    assert engine.focused is None
    assert engine.registered == ()


def test_first_widget_gets_focus() -> None:
    engine = FocusEngine()

    engine.register("solar")

    assert engine.focused == "solar"


def test_register_is_idempotent() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.register("solar")

    assert engine.registered == ("solar",)


def test_focus_widget() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.register("battery")

    assert engine.focus("battery")
    assert engine.focused == "battery"


def test_focus_unknown_widget() -> None:
    engine = FocusEngine()

    assert not engine.focus("missing")


def test_next_focus_wraps() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.register("battery")

    assert engine.next() == "battery"
    assert engine.next() == "solar"


def test_previous_focus_wraps() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.register("battery")

    assert engine.previous() == "battery"
    assert engine.previous() == "solar"


def test_unregister_focused_widget() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.register("battery")
    engine.focus("battery")

    engine.unregister("battery")

    assert engine.focused == "solar"


def test_unregister_unknown_widget() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.unregister("missing")

    assert engine.focused == "solar"


def test_clear_focus() -> None:
    engine = FocusEngine()

    engine.register("solar")
    engine.clear()

    assert engine.focused is None
    assert engine.registered == ("solar",)