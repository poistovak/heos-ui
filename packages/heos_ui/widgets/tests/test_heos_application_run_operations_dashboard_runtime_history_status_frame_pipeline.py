import importlib

pipeline_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_frame_pipeline"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

Pipeline = (
    pipeline_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFramePipeline
)
FrameResult = (
    pipeline_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusFrameResult
)
View = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)
Severity = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity
)


def view(
    *,
    title: str = "HEOS Runtime History",
    status: str = "RUNNING",
    detail: str = "Runtime history orchestration is active.",
    cycles: str = "Cycles 3",
    runs: str = "Runs 3",
    refreshes: str = "Refreshes 3",
    latest: str = "Latest sequence 3",
    severity: Severity = Severity.ACTIVE,
) -> View:
    return View(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        runs=runs,
        refreshes=refreshes,
        latest=latest,
        severity=severity,
    )


def test_create_builds_renderer() -> None:
    pipeline = Pipeline.create()

    assert pipeline.renderer is not None


def test_create_builds_canvas_renderer() -> None:
    pipeline = Pipeline.create()

    assert pipeline.canvas_renderer is not None


def test_render_returns_frame_result() -> None:
    result = Pipeline.create().render(view())

    assert isinstance(result, FrameResult)


def test_render_result_contains_scene() -> None:
    result = Pipeline.create().render(view())

    assert result.scene.title == "HEOS Runtime History"
    assert result.scene.status == "RUNNING"


def test_render_result_contains_frame() -> None:
    result = Pipeline.create().render(view())

    assert result.frame.command_count == 7


def test_pipeline_preserves_title() -> None:
    result = Pipeline.create().render(
        view(title="HEOS History Observatory")
    )

    assert result.scene.title == "HEOS History Observatory"
    assert result.frame.commands[0].text == "HEOS History Observatory"


def test_pipeline_preserves_status() -> None:
    result = Pipeline.create().render(
        view(status="RUNNING")
    )

    assert result.scene.status == "RUNNING"
    assert result.frame.commands[1].text == "RUNNING"


def test_pipeline_preserves_counts() -> None:
    result = Pipeline.create().render(
        view(
            cycles="Cycles 246",
            runs="Runs 245",
            refreshes="Refreshes 244",
        )
    )

    assert result.frame.commands[3].text == "Cycles: Cycles 246"
    assert result.frame.commands[4].text == "Runs: Runs 245"
    assert result.frame.commands[5].text == "Refreshes: Refreshes 244"


def test_pipeline_preserves_latest() -> None:
    result = Pipeline.create().render(
        view(latest="Latest sequence 246")
    )

    assert result.frame.commands[6].text == "Latest: Latest sequence 246"


def test_pipeline_preserves_severity() -> None:
    result = Pipeline.create().render(
        view(severity=Severity.STOPPED)
    )

    assert result.scene.severity is Severity.STOPPED


def test_idle_view_flows_through_pipeline() -> None:
    result = Pipeline.create().render(
        view(
            status="IDLE",
            detail="Runtime history has not produced an update.",
            cycles="Cycles 0",
            runs="Runs 0",
            refreshes="Refreshes 0",
            latest="Latest sequence —",
            severity=Severity.NEUTRAL,
        )
    )

    assert result.scene.status == "IDLE"
    assert result.frame.commands[1].text == "IDLE"
    assert result.frame.commands[6].text == "Latest: Latest sequence —"


def test_stopped_view_flows_through_pipeline() -> None:
    result = Pipeline.create().render(
        view(
            status="STOPPED",
            detail="Runtime history orchestration is stopped.",
            severity=Severity.STOPPED,
        )
    )

    assert result.scene.status == "STOPPED"
    assert result.frame.commands[1].text == "STOPPED"


def test_result_is_snapshot() -> None:
    source = view(
        cycles="Cycles 1",
        latest="Latest sequence 1",
    )

    result = Pipeline.create().render(source)

    assert result.scene.fields[1].value == "Cycles 1"
    assert result.frame.commands[3].text == "Cycles: Cycles 1"
    assert result.frame.commands[6].text == "Latest: Latest sequence 1"


def test_pipeline_is_repeatable() -> None:
    pipeline = Pipeline.create()
    source = view()

    first = pipeline.render(source)
    second = pipeline.render(source)

    assert first == second
    assert first is not second


def test_scene_and_frame_are_synchronized() -> None:
    result = Pipeline.create().render(
        view(
            cycles="Cycles 246",
            latest="Latest sequence 246",
        )
    )

    assert result.scene.fields[1].value == "Cycles 246"
    assert result.frame.commands[3].text == "Cycles: Cycles 246"
    assert result.scene.fields[4].value == "Latest sequence 246"
    assert result.frame.commands[6].text == "Latest: Latest sequence 246"
