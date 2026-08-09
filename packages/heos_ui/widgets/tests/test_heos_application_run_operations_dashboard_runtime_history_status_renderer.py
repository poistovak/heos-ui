import importlib

renderer_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_renderer"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)

Renderer = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderer
)
RenderField = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField
)
RenderScene = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderScene
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


def test_renderer_returns_scene() -> None:
    scene = Renderer().render(view())

    assert isinstance(scene, RenderScene)


def test_renderer_preserves_title() -> None:
    scene = Renderer().render(
        view(title="HEOS History Observatory")
    )

    assert scene.title == "HEOS History Observatory"


def test_renderer_preserves_status() -> None:
    scene = Renderer().render(
        view(status="RUNNING")
    )

    assert scene.status == "RUNNING"


def test_renderer_preserves_severity() -> None:
    scene = Renderer().render(
        view(severity=Severity.ACTIVE)
    )

    assert scene.severity is Severity.ACTIVE


def test_renderer_creates_detail_field() -> None:
    scene = Renderer().render(
        view(detail="Runtime history orchestration is active.")
    )

    field = scene.fields[0]

    assert isinstance(field, RenderField)
    assert field.label == "Detail"
    assert field.value == "Runtime history orchestration is active."


def test_renderer_creates_cycles_field() -> None:
    scene = Renderer().render(
        view(cycles="Cycles 244")
    )

    assert scene.fields[1].label == "Cycles"
    assert scene.fields[1].value == "Cycles 244"


def test_renderer_creates_runs_field() -> None:
    scene = Renderer().render(
        view(runs="Runs 244")
    )

    assert scene.fields[2].label == "Runs"
    assert scene.fields[2].value == "Runs 244"


def test_renderer_creates_refreshes_field() -> None:
    scene = Renderer().render(
        view(refreshes="Refreshes 244")
    )

    assert scene.fields[3].label == "Refreshes"
    assert scene.fields[3].value == "Refreshes 244"


def test_renderer_creates_latest_field() -> None:
    scene = Renderer().render(
        view(latest="Latest sequence 244")
    )

    assert scene.fields[4].label == "Latest"
    assert scene.fields[4].value == "Latest sequence 244"


def test_renderer_creates_five_fields() -> None:
    scene = Renderer().render(view())

    assert scene.field_count == 5
    assert len(scene.fields) == 5


def test_renderer_preserves_field_order() -> None:
    scene = Renderer().render(view())

    assert tuple(field.label for field in scene.fields) == (
        "Detail",
        "Cycles",
        "Runs",
        "Refreshes",
        "Latest",
    )


def test_stopped_view_renders_stopped_scene() -> None:
    scene = Renderer().render(
        view(
            status="STOPPED",
            detail="Runtime history orchestration is stopped.",
            severity=Severity.STOPPED,
        )
    )

    assert scene.status == "STOPPED"
    assert scene.severity is Severity.STOPPED


def test_idle_view_renders_neutral_scene() -> None:
    scene = Renderer().render(
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

    assert scene.status == "IDLE"
    assert scene.severity is Severity.NEUTRAL
    assert scene.fields[4].value == "Latest sequence —"


def test_render_scene_is_snapshot() -> None:
    source = view(
        cycles="Cycles 244",
        runs="Runs 244",
        refreshes="Refreshes 244",
        latest="Latest sequence 244",
    )

    scene = Renderer().render(source)

    assert scene.fields[1].value == "Cycles 244"
    assert scene.fields[2].value == "Runs 244"
    assert scene.fields[3].value == "Refreshes 244"
    assert scene.fields[4].value == "Latest sequence 244"


def test_renderer_is_repeatable() -> None:
    renderer = Renderer()
    source = view()

    first = renderer.render(source)
    second = renderer.render(source)

    assert first == second
    assert first is not second
