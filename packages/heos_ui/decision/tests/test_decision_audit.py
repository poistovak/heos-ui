from heos_ui.decision import Action, Decision, DecisionAction
from heos_ui.decision.audit import (
    DecisionAuditTrail,
    DecisionOutcome,
)
from heos_ui.energy import EnergySnapshot


def candidate(
    target: str = "wattpilot",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target=target,
            action="set_current",
            reason="PV surplus available.",
        ),
        action=Action(
            priority=100,
            target=target,
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def test_audit_starts_empty() -> None:
    audit = DecisionAuditTrail()

    assert audit.count == 0
    assert audit.records() == ()


def test_record_decision() -> None:
    audit = DecisionAuditTrail()
    snapshot = EnergySnapshot(
        pv_power=6000.0,
        house_power=2000.0,
    )

    record = audit.record(
        snapshot,
        candidate(),
        DecisionOutcome(
            success=True,
            message="Command executed.",
        ),
    )

    assert audit.count == 1
    assert record.snapshot == snapshot
    assert record.outcome.success


def test_successful_records() -> None:
    audit = DecisionAuditTrail()
    snapshot = EnergySnapshot()

    audit.record(
        snapshot,
        candidate(),
        DecisionOutcome(success=True),
    )

    assert len(audit.successful()) == 1
    assert audit.failed() == ()


def test_failed_records() -> None:
    audit = DecisionAuditTrail()
    snapshot = EnergySnapshot()

    audit.record(
        snapshot,
        candidate(),
        DecisionOutcome(
            success=False,
            message="Device unavailable.",
        ),
    )

    assert len(audit.failed()) == 1
    assert audit.successful() == ()


def test_filter_by_target() -> None:
    audit = DecisionAuditTrail()
    snapshot = EnergySnapshot()

    audit.record(
        snapshot,
        candidate("wattpilot"),
        DecisionOutcome(success=True),
    )
    audit.record(
        snapshot,
        candidate("daikin"),
        DecisionOutcome(success=True),
    )

    records = audit.for_target("wattpilot")

    assert len(records) == 1
    assert records[0].candidate.action.target == "wattpilot"


def test_timestamp_is_created() -> None:
    audit = DecisionAuditTrail()

    record = audit.record(
        EnergySnapshot(),
        candidate(),
        DecisionOutcome(success=True),
    )

    assert record.timestamp.tzinfo is not None


def test_clear() -> None:
    audit = DecisionAuditTrail()

    audit.record(
        EnergySnapshot(),
        candidate(),
        DecisionOutcome(success=True),
    )

    audit.clear()

    assert audit.count == 0
    assert audit.records() == ()