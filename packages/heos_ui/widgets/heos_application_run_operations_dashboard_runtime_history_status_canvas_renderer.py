from __future__ import annotations

import importlib
from dataclasses import dataclass

renderer_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_renderer"
)

RenderScene = (
    renderer_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderScene
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasCommand:
    text: str
    row: int


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasFrame:
    commands: tuple[
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasCommand,
        ...,
    ]

    @property
    def command_count(self) -> int:
        return len(self.commands)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasRenderer:
    def render(
        self,
        scene: RenderScene,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasFrame:
        commands = [
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasCommand(
                text=scene.title,
                row=0,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasCommand(
                text=scene.status,
                row=1,
            ),
        ]

        for row, field in enumerate(scene.fields, start=2):
            commands.append(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasCommand(
                    text=f"{field.label}: {field.value}",
                    row=row,
                )
            )

        return (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusCanvasFrame(
                commands=tuple(commands),
            )
        )
