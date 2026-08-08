from __future__ import annotations

from dataclasses import dataclass

from .brain_runtime_history import BrainRuntimeHistory
from .brain_runtime_lifecycle import BrainRuntimeLifecycleState


@dataclass(frozen=True, slots=True)
class BrainRuntimeMetricsSnapshot:
    total: int
    created: int
    started: int
    running: int
    stopped: int
    attention: int
    healthy: int
    latest_cycle: int | None
    max_cycle: int | None

    @property
    def active(self) -> int:
        return self.started + self.running

    @property
    def attention_ratio(self) -> float:
        if self.total == 0:
            return 0.0

        return self.attention / self.total


@dataclass(frozen=True, slots=True)
class BrainRuntimeMetrics:
    def analyze(
        self,
        history: BrainRuntimeHistory,
    ) -> BrainRuntimeMetricsSnapshot:
        states = history.states

        created = sum(
            state.lifecycle is BrainRuntimeLifecycleState.CREATED
            for state in states
        )
        started = sum(
            state.lifecycle is BrainRuntimeLifecycleState.STARTED
            for state in states
        )
        running = sum(
            state.lifecycle is BrainRuntimeLifecycleState.RUNNING
            for state in states
        )
        stopped = sum(
            state.lifecycle is BrainRuntimeLifecycleState.STOPPED
            for state in states
        )

        attention = sum(
            state.status == "ATTENTION"
            for state in states
        )
        healthy = sum(
            state.status == "RUNNING"
            for state in states
        )

        cycles = tuple(
            state.cycle
            for state in states
            if state.cycle is not None
        )

        latest_cycle = (
            history.latest.cycle
            if history.latest is not None
            else None
        )

        return BrainRuntimeMetricsSnapshot(
            total=len(states),
            created=created,
            started=started,
            running=running,
            stopped=stopped,
            attention=attention,
            healthy=healthy,
            latest_cycle=latest_cycle,
            max_cycle=max(cycles) if cycles else None,
        )
