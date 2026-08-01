from heos_ui.runtime import FrameBudget


def test_budget_accepts_fast_frame() -> None:
    budget = FrameBudget(16.67)

    assert budget.within_budget(12.0)


def test_budget_rejects_slow_frame() -> None:
    budget = FrameBudget(16.67)

    assert not budget.within_budget(18.0)


def test_remaining_budget() -> None:
    budget = FrameBudget(16.67)

    assert budget.remaining(10.0) == 6.67


def test_remaining_never_negative() -> None:
    budget = FrameBudget(16.67)

    assert budget.remaining(20.0) == 0.0


def test_exceeded_by() -> None:
    budget = FrameBudget(16.67)

    assert budget.exceeded_by(20.0) == 3.33


def test_not_exceeded() -> None:
    budget = FrameBudget(16.67)

    assert budget.exceeded_by(12.0) == 0.0