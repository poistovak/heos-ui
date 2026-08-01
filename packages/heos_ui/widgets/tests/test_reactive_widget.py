from heos_ui.widgets.base import Widget


class RecordingWidget(Widget):
    def __init__(self, widget_id: str, title: str) -> None:
        super().__init__(id=widget_id, title=title)
        self.rendered_titles: list[str] = []

    def render(self) -> None:
        self.rendered_titles.append(self.title)


def test_widget_is_clean_initially() -> None:
    widget = Widget(id="pv", title="PV Power")

    assert widget.dirty is False
    assert widget.render_count == 0


def test_invalidate_marks_widget_dirty() -> None:
    widget = Widget(id="pv", title="PV Power")

    changed = widget.invalidate()

    assert changed is True
    assert widget.dirty is True


def test_repeated_invalidation_does_not_duplicate_work() -> None:
    widget = Widget(id="pv", title="PV Power")

    first = widget.invalidate()
    second = widget.invalidate()
    third = widget.invalidate()

    assert first is True
    assert second is False
    assert third is False
    assert widget.dirty is True


def test_render_if_dirty_does_nothing_for_clean_widget() -> None:
    widget = RecordingWidget("pv", "PV Power")

    rendered = widget.render_if_dirty()

    assert rendered is False
    assert widget.rendered_titles == []
    assert widget.render_count == 0


def test_render_if_dirty_renders_dirty_widget() -> None:
    widget = RecordingWidget("pv", "PV Power")
    widget.invalidate()

    rendered = widget.render_if_dirty()

    assert rendered is True
    assert widget.rendered_titles == ["PV Power"]
    assert widget.dirty is False
    assert widget.render_count == 1


def test_dirty_widget_renders_only_once() -> None:
    widget = RecordingWidget("pv", "PV Power")

    widget.invalidate()

    first = widget.render_if_dirty()
    second = widget.render_if_dirty()

    assert first is True
    assert second is False
    assert widget.rendered_titles == ["PV Power"]
    assert widget.render_count == 1


def test_widget_can_be_invalidated_again_after_render() -> None:
    widget = RecordingWidget("pv", "PV Power")

    widget.invalidate()
    widget.render_if_dirty()

    widget.invalidate()
    widget.render_if_dirty()

    assert widget.rendered_titles == [
        "PV Power",
        "PV Power",
    ]
    assert widget.render_count == 2