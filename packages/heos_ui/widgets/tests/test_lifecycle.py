import pytest
from heos_ui.widgets import Widget, WidgetLifecycle


def test_widget_starts_created() -> None:
    widget = Widget(id="power", title="Power")

    assert widget.lifecycle is WidgetLifecycle.CREATED


def test_widget_lifecycle_transitions() -> None:
    widget = Widget(id="power", title="Power")

    widget.attach()
    assert widget.lifecycle is WidgetLifecycle.ATTACHED

    widget.show()
    assert widget.lifecycle is WidgetLifecycle.VISIBLE

    widget.hide()
    assert widget.lifecycle is WidgetLifecycle.HIDDEN

    widget.show()
    assert widget.lifecycle is WidgetLifecycle.VISIBLE

    widget.dispose()
    assert widget.lifecycle is WidgetLifecycle.DISPOSED


def test_invalid_widget_transition_raises_error() -> None:
    widget = Widget(id="power", title="Power")

    with pytest.raises(RuntimeError):
        widget.show()


def test_dispose_is_idempotent() -> None:
    widget = Widget(id="power", title="Power")

    widget.dispose()
    widget.dispose()

    assert widget.lifecycle is WidgetLifecycle.DISPOSED