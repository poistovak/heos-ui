import pytest
from heos_ui.widgets import (
    LabelWidget,
    ValueWidget,
    Widget,
    WidgetLifecycle,
)


def test_label_widget_renders_text() -> None:
    widget = LabelWidget(
        id="status",
        title="Status",
        text="System ready",
    )

    assert widget.render() == "System ready"


def test_value_widget_renders_value_without_unit() -> None:
    widget = ValueWidget(
        id="battery",
        title="Battery",
        value=82,
        unit="",
    )

    assert widget.render() == "82"


def test_value_widget_renders_value_with_unit() -> None:
    widget = ValueWidget(
        id="solar-power",
        title="Solar power",
        value=8.4,
        unit="kW",
    )

    assert widget.render() == "8.4 kW"


def test_widget_metadata_defaults() -> None:
    widget = Widget(
        id="solar",
        title="Solar",
    )

    assert widget.description == ""
    assert widget.enabled is True
    assert widget.visible is False


def test_widget_becomes_visible_after_show() -> None:
    widget = Widget(
        id="solar",
        title="Solar",
    )

    widget.attach()
    widget.show()

    assert widget.visible is True
    assert widget.lifecycle is WidgetLifecycle.VISIBLE


def test_disabling_visible_widget_hides_it() -> None:
    widget = Widget(
        id="solar",
        title="Solar",
    )

    widget.attach()
    widget.show()
    widget.disable()

    assert widget.enabled is False
    assert widget.visible is False
    assert widget.lifecycle is WidgetLifecycle.HIDDEN


def test_disabled_widget_cannot_be_shown() -> None:
    widget = Widget(
        id="solar",
        title="Solar",
    )

    widget.attach()
    widget.disable()

    with pytest.raises(
        RuntimeError,
        match="Cannot show a disabled widget.",
    ):
        widget.show()


def test_disposed_widget_cannot_be_enabled() -> None:
    widget = Widget(
        id="solar",
        title="Solar",
    )
    widget.dispose()

    with pytest.raises(
        RuntimeError,
        match="Cannot modify a disposed widget.",
    ):
        widget.enable()


