from heos_ui.decision import Action, Decision, DecisionAction
from heos_ui.decision.trace import DecisionTrace


def candidate() -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target="wattpilot",
            action="set_current",
            reason="PV surplus available.",
        ),
        action=Action(
            priority=100,
            target="wattpilot",
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def test_starts_empty() -> None:
    trace = DecisionTrace()

    assert trace.count == 0
    assert trace.entries() == ()


def test_record_accepted() -> None:
    trace = DecisionTrace()

    entry = trace.record(
        candidate(),
        accepted=True,
        reason="Highest priority.",
    )

    assert entry.accepted
    assert trace.count == 1


def test_record_rejected() -> None:
    trace = DecisionTrace()

    trace.record(
        candidate(),
        accepted=False,
        reason="Higher priority candidate exists.",
    )

    assert len(trace.rejected()) == 1


def test_filter_accepted() -> None:
    trace = DecisionTrace()
    item = candidate()

    trace.record(
        item,
        accepted=True,
        reason="Winner.",
    )
    trace.record(
        item,
        accepted=False,
        reason="Conflict.",
    )

    assert len(trace.accepted()) == 1
    assert len(trace.rejected()) == 1


def test_reason_is_preserved() -> None:
    trace = DecisionTrace()

    entry = trace.record(
        candidate(),
        accepted=True,
        reason="PV surplus exceeds threshold.",
    )

    assert entry.reason == "PV surplus exceeds threshold."


def test_timestamp_is_created() -> None:
    trace = DecisionTrace()

    entry = trace.record(
        candidate(),
        accepted=True,
        reason="Winner.",
    )

    assert entry.timestamp.tzinfo is not None


def test_clear() -> None:
    trace = DecisionTrace()

    trace.record(
        candidate(),
        accepted=True,
        reason="Winner.",
    )

    trace.clear()

    assert trace.count == 0