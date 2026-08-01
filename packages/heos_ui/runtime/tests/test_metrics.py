from heos_ui.runtime import RenderMetrics


def test_metrics_start_empty() -> None:
    metrics = RenderMetrics(
        frames=0,
        rendered_widgets=0,
        skipped_widgets=0,
    )

    assert metrics.total_widgets == 0
    assert metrics.render_ratio == 0.0


def test_total_widgets() -> None:
    metrics = RenderMetrics(
        frames=5,
        rendered_widgets=12,
        skipped_widgets=8,
    )

    assert metrics.total_widgets == 20


def test_render_ratio() -> None:
    metrics = RenderMetrics(
        frames=2,
        rendered_widgets=6,
        skipped_widgets=2,
    )

    assert metrics.render_ratio == 0.75


def test_all_widgets_rendered() -> None:
    metrics = RenderMetrics(
        frames=3,
        rendered_widgets=9,
        skipped_widgets=0,
    )

    assert metrics.render_ratio == 1.0


def test_no_widgets_rendered() -> None:
    metrics = RenderMetrics(
        frames=4,
        rendered_widgets=0,
        skipped_widgets=5,
    )

    assert metrics.render_ratio == 0.0