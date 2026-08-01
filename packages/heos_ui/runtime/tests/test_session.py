from heos_ui.runtime import (
    FrameClock,
    RenderContext,
    RenderDiagnostics,
    RenderLifecycle,
    RenderMetrics,
    RenderProfilerSnapshot,
    RenderSession,
    RenderStatistics,
)


def create_session() -> RenderSession:
    return RenderSession(
        context=RenderContext(
            clock=FrameClock(frame=12),
            lifecycle=RenderLifecycle(
                frame=12,
                active=True,
            ),
            diagnostics=RenderDiagnostics(
                statistics=RenderStatistics(
                    attempted=20,
                    rendered=18,
                    skipped=2,
                    batches=5,
                ),
                metrics=RenderMetrics(
                    frames=12,
                    rendered_widgets=18,
                    skipped_widgets=2,
                ),
                profiler=RenderProfilerSnapshot(
                    frame_count=12,
                    total_frame_time=18.0,
                    average_frame_time=1.5,
                    last_frame_time=1.4,
                ),
            ),
        )
    )


def test_session_starts_empty() -> None:
    session = create_session()

    assert session.frames_rendered == 0


def test_begin_frame() -> None:
    session = create_session()

    session.begin_frame()
    session.begin_frame()

    assert session.frames_rendered == 2


def test_current_frame() -> None:
    assert create_session().current_frame == 12


def test_active() -> None:
    assert create_session().active is True


def test_context_reference() -> None:
    assert create_session().context.clock.frame == 12


def test_statistics_reference() -> None:
    assert (
        create_session()
        .context
        .diagnostics
        .statistics
        .rendered
        == 18
    )