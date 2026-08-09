import importlib

orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

Orchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
Presenter = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresenter
)
Presentation = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresentation
)
Severity = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


def test_present_returns_presentation() -> None:
    orchestrator = Orchestrator.create()
    snapshot = Snapshot.capture(orchestrator)

    presentation = Presenter().present(snapshot)

    assert isinstance(presentation, Presentation)


def test_initial_snapshot_is_presented_as_idle() -> None:
    orchestrator = Orchestrator.create()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.status == "IDLE"
    assert presentation.severity is Severity.NEUTRAL


def test_initial_detail_describes_no_updates() -> None:
    orchestrator = Orchestrator.create()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.detail == (
        "Runtime history has not produced an update."
    )


def test_initial_counts_are_zero() -> None:
    orchestrator = Orchestrator.create()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.cycles == "Cycles 0"
    assert presentation.runs == "Runs 0"
    assert presentation.refreshes == "Refreshes 0"


def test_initial_latest_sequence_is_empty() -> None:
    orchestrator = Orchestrator.create()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.latest == "Latest sequence —"


def test_started_orchestrator_is_presented_as_running() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.status == "RUNNING"
    assert presentation.severity is Severity.ACTIVE


def test_running_detail_describes_active_orchestration() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.detail == (
        "Runtime history orchestration is active."
    )


def test_one_cycle_is_presented() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    orchestrator.cycle()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.cycles == "Cycles 1"
    assert presentation.runs == "Runs 1"
    assert presentation.refreshes == "Refreshes 1"
    assert presentation.latest == "Latest sequence 1"


def test_multiple_cycles_are_presented() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()

    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.cycle()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.cycles == "Cycles 3"
    assert presentation.runs == "Runs 3"
    assert presentation.refreshes == "Refreshes 3"
    assert presentation.latest == "Latest sequence 3"


def test_stopped_orchestrator_with_history_is_stopped() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    orchestrator.cycle()
    orchestrator.stop()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.status == "STOPPED"
    assert presentation.severity is Severity.STOPPED


def test_stopped_detail_is_presented() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    orchestrator.cycle()
    orchestrator.stop()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.detail == (
        "Runtime history orchestration is stopped."
    )


def test_stopped_state_preserves_counts() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    orchestrator.cycle()
    orchestrator.cycle()
    orchestrator.stop()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.cycles == "Cycles 2"
    assert presentation.runs == "Runs 2"
    assert presentation.refreshes == "Refreshes 2"
    assert presentation.latest == "Latest sequence 2"


def test_reset_returns_presentation_to_idle() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    orchestrator.cycle()
    orchestrator.reset()

    presentation = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.status == "IDLE"
    assert presentation.severity is Severity.NEUTRAL
    assert presentation.cycles == "Cycles 0"
    assert presentation.latest == "Latest sequence —"


def test_custom_title_is_preserved() -> None:
    orchestrator = Orchestrator.create()

    presentation = Presenter(
        title="HEOS History Observatory"
    ).present(
        Snapshot.capture(orchestrator)
    )

    assert presentation.title == "HEOS History Observatory"


def test_presentation_is_snapshot() -> None:
    orchestrator = Orchestrator.create()
    orchestrator.start()
    orchestrator.cycle()

    first = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    orchestrator.cycle()

    second = Presenter().present(
        Snapshot.capture(orchestrator)
    )

    assert first.cycles == "Cycles 1"
    assert first.latest == "Latest sequence 1"
    assert second.cycles == "Cycles 2"
    assert second.latest == "Latest sequence 2"
