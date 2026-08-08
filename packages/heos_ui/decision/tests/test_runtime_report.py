from heos_ui.decision import (
    Action,
    Decision,
    DecisionAction,
)
from heos_ui.decision.guarded_pipeline import (
    BlockedDecision,
    GuardedDecisionResult,
)
from heos_ui.decision.runtime import DecisionRuntimeResult
from heos_ui.decision.runtime_report import RuntimeExecutionReport


def candidate(
    target: str = "wattpilot",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target=target,
            action="set_current",
            reason="Runtime report test.",
        ),
        action=Action(
            priority=100,
            target=target,
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def runtime_result(
    *,
    accepted: tuple[DecisionAction, ...] = (),
    blocked: tuple[BlockedDecision, ...] = (),
    executed: int = 0,
) -> DecisionRuntimeResult:
    return DecisionRuntimeResult(
        guarded=GuardedDecisionResult(
            accepted=accepted,
            blocked=blocked,
        ),
        executed=executed,
    )


def test_empty_report() -> None:
    report = RuntimeExecutionReport.from_result(
        runtime_result()
    )

    assert report.accepted == 0
    assert report.blocked == 0
    assert report.executed == 0
    assert report.total == 0


def test_accepted_count() -> None:
    item = candidate()

    report = RuntimeExecutionReport.from_result(
        runtime_result(
            accepted=(item,),
            executed=1,
        )
    )

    assert report.accepted == 1
    assert report.executed == 1


def test_blocked_count() -> None:
    item = candidate()

    blocked = BlockedDecision(
        candidate=item,
        reason="Target is in backoff.",
    )

    report = RuntimeExecutionReport.from_result(
        runtime_result(
            blocked=(blocked,),
        )
    )

    assert report.blocked == 1
    assert report.has_blocked


def test_total_counts_accepted_and_blocked() -> None:
    accepted = candidate("daikin")
    rejected = candidate("wattpilot")

    blocked = BlockedDecision(
        candidate=rejected,
        reason="Target is in backoff.",
    )

    report = RuntimeExecutionReport.from_result(
        runtime_result(
            accepted=(accepted,),
            blocked=(blocked,),
            executed=1,
        )
    )

    assert report.total == 2


def test_fully_executed() -> None:
    item = candidate()

    report = RuntimeExecutionReport.from_result(
        runtime_result(
            accepted=(item,),
            executed=1,
        )
    )

    assert report.fully_executed


def test_not_fully_executed_when_blocked() -> None:
    item = candidate()

    blocked = BlockedDecision(
        candidate=item,
        reason="Target is not registered.",
    )

    report = RuntimeExecutionReport.from_result(
        runtime_result(
            blocked=(blocked,),
        )
    )

    assert not report.fully_executed


def test_not_fully_executed_when_execution_is_missing() -> None:
    item = candidate()

    report = RuntimeExecutionReport.from_result(
        runtime_result(
            accepted=(item,),
            executed=0,
        )
    )

    assert not report.fully_executed