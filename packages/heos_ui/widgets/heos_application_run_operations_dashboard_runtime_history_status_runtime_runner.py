from __future__ import annotations

import importlib
from dataclasses import dataclass

bridge_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_runtime_bridge"
)

Bridge = (
    bridge_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeBridge
)
RuntimeStep = (
    bridge_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult:
    steps: tuple[RuntimeStep, ...]

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def latest(self) -> RuntimeStep | None:
        if not self.steps:
            return None

        return self.steps[-1]


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeRunner:
    bridge: Bridge
    _run_count: int = 0
    _latest: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult
        | None
    ) = None

    @classmethod
    def create(
        cls,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeRunner
    ):
        return cls(
            bridge=Bridge.create(),
        )

    @property
    def running(self) -> bool:
        return self.bridge.running

    @property
    def run_count(self) -> int:
        return self._run_count

    @property
    def latest(
        self,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult
        | None
    ):
        return self._latest

    @property
    def has_runs(self) -> bool:
        return self._latest is not None

    def start(self) -> None:
        self.bridge.start()

    def run(
        self,
        steps: int,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult:
        if not self.running:
            raise RuntimeError(
                "Runtime history status runner is not running."
            )

        if steps < 0:
            raise ValueError(
                "Runtime history status runner steps cannot be negative."
            )

        results = tuple(
            self.bridge.step()
            for _ in range(steps)
        )

        self._run_count += 1

        result = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult(
                steps=results,
            )
        )

        self._latest = result
        return result

    def stop(self) -> None:
        self.bridge.stop()

    def reset(self) -> None:
        self.bridge.reset()
        self._run_count = 0
        self._latest = None
