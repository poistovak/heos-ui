from __future__ import annotations

import importlib
from dataclasses import dataclass

application_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_application"
)

Application = (
    application_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusApplication
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep:
    sequence: int
    runtime_update: object
    status_update: object


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeBridge:
    application: Application
    _step_count: int = 0
    _latest: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep
        | None
    ) = None

    @classmethod
    def create(
        cls,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeBridge
    ):
        return cls(
            application=Application.create(),
        )

    @property
    def running(self) -> bool:
        return self.application.running

    @property
    def step_count(self) -> int:
        return self._step_count

    @property
    def latest(
        self,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep
        | None
    ):
        return self._latest

    @property
    def has_steps(self) -> bool:
        return self._latest is not None

    def start(self) -> None:
        self.application.launch()

    def step(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep:
        if not self.running:
            raise RuntimeError(
                "Runtime history status bridge is not running."
            )

        runtime_update = (
            self.application.supervisor.orchestrator.cycle()
        )
        status_update = self.application.update()

        self._step_count += 1

        step = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRuntimeStep(
                sequence=self._step_count,
                runtime_update=runtime_update,
                status_update=status_update,
            )
        )

        self._latest = step
        return step

    def stop(self) -> None:
        self.application.shutdown()

    def reset(self) -> None:
        self.application.reset()
        self._step_count = 0
        self._latest = None
