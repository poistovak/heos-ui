from heos_ui.widgets.brain_runtime_health import (
    BrainRuntimeHealthAssessor,
    BrainRuntimeHealthLevel,
)
from heos_ui.widgets.brain_runtime_metrics import BrainRuntimeMetricsSnapshot


def metrics(
    *,
    total: int = 4,
    attention: int = 0,
    latest_cycle: int | None = 172,
) -> BrainRuntimeMetricsSnapshot:
    healthy = max(total - attention, 0)

    return BrainRuntimeMetricsSnapshot(
        total=total,
        created=0,
        started=0,
        running=total,
        stopped=0,
        attention=attention,
        healthy=healthy,
        latest_cycle=latest_cycle,
        max_cycle=latest_cycle,
    )


def test_empty_metrics_are_unknown() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=0,
            attention=0,
            latest_cycle=None,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.UNKNOWN
    assert not health.healthy
    assert not health.requires_attention


def test_zero_attention_is_healthy() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=10,
            attention=0,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.HEALTHY
    assert health.healthy
    assert not health.requires_attention


def test_low_attention_ratio_is_degraded() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=10,
            attention=2,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.DEGRADED
    assert not health.healthy
    assert health.requires_attention


def test_half_attention_ratio_is_critical() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=10,
            attention=5,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.CRITICAL
    assert health.requires_attention


def test_high_attention_ratio_is_critical() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=10,
            attention=8,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.CRITICAL


def test_health_preserves_total_states() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=12,
            attention=3,
        )
    )

    assert health.total_states == 12


def test_health_preserves_attention_states() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=12,
            attention=3,
        )
    )

    assert health.attention_states == 3


def test_health_preserves_attention_ratio() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            total=4,
            attention=1,
        )
    )

    assert health.attention_ratio == 0.25


def test_health_preserves_latest_cycle() -> None:
    health = BrainRuntimeHealthAssessor().assess(
        metrics(
            latest_cycle=172,
        )
    )

    assert health.latest_cycle == 172


def test_custom_critical_threshold_is_supported() -> None:
    assessor = BrainRuntimeHealthAssessor(
        critical_attention_ratio=0.75,
    )

    health = assessor.assess(
        metrics(
            total=10,
            attention=6,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.DEGRADED


def test_custom_threshold_can_make_state_critical() -> None:
    assessor = BrainRuntimeHealthAssessor(
        critical_attention_ratio=0.25,
    )

    health = assessor.assess(
        metrics(
            total=10,
            attention=3,
        )
    )

    assert health.level is BrainRuntimeHealthLevel.CRITICAL
