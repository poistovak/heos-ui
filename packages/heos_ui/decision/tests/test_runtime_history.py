from heos_ui.decision.runtime_cycle import RuntimeCycleResult
from heos_ui.decision.runtime_history import RuntimeCycleHistory
from heos_ui.decision.runtime_report import RuntimeExecutionReport


def cycle_result(
    *,
    accepted: int = 0,
    blocked: int = 0,
    executed: int = 0,
) -> RuntimeCycleResult:
    report = RuntimeExecutionReport(
        accepted=accepted,
        blocked=blocked,
        executed=executed,
    )

    return RuntimeCycleResult(report=report)


def test_history_starts_empty() -> None:
    history = RuntimeCycleHistory()

    assert history.count == 0
    assert history.records() == ()
    assert history.latest() is None


def test_record_cycle() -> None:
    history = RuntimeCycleHistory()

    entry = history.record(
        cycle_result(
            accepted=1,
            executed=1,
        )
    )

    assert history.count == 1
    assert entry.sequence == 1
    assert entry.result.successful


def test_sequence_increments() -> None:
    history = RuntimeCycleHistory()

    first = history.record(cycle_result())
    second = history.record(cycle_result())
    third = history.record(cycle_result())

    assert first.sequence == 1
    assert second.sequence == 2
    assert third.sequence == 3


def test_latest_returns_last_cycle() -> None:
    history = RuntimeCycleHistory()

    history.record(cycle_result())
    second = history.record(
        cycle_result(
            accepted=1,
            executed=1,
        )
    )

    assert history.latest() == second


def test_successful_cycles_are_filtered() -> None:
    history = RuntimeCycleHistory()

    history.record(
        cycle_result(
            accepted=1,
            executed=1,
        )
    )
    history.record(
        cycle_result(
            blocked=1,
        )
    )
    history.record(
        cycle_result(
            accepted=2,
            executed=2,
        )
    )

    successful = history.successful()

    assert len(successful) == 2
    assert successful[0].sequence == 1
    assert successful[1].sequence == 3


def test_failed_cycles_are_filtered() -> None:
    history = RuntimeCycleHistory()

    history.record(
        cycle_result(
            accepted=1,
            executed=1,
        )
    )
    history.record(
        cycle_result(
            blocked=1,
        )
    )

    failed = history.failed()

    assert len(failed) == 1
    assert failed[0].sequence == 2


def test_clear_removes_history() -> None:
    history = RuntimeCycleHistory()

    history.record(cycle_result())
    history.record(cycle_result())

    history.clear()

    assert history.count == 0
    assert history.records() == ()
    assert history.latest() is None