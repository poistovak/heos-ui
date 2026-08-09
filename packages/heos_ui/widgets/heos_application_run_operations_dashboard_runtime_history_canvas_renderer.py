from __future__ import annotations

from dataclasses import dataclass

from . import (
    heos_application_run_operations_dashboard_runtime_history_health_renderer as history_renderer,
)

RenderScene = (
    history_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasCommand:
    text: str
    row: int


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasFrame:
    commands: tuple[
        HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasCommand,
        ...,
    ]

    @property
    def command_count(self) -> int:
        return len(self.commands)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasRenderer:
    def render(
        self,
        scene: RenderScene,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasFrame:
        commands = [
            HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasCommand(
                text=scene.title,
                row=0,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasCommand(
                text=scene.status,
                row=1,
            ),
        ]

        for row, field in enumerate(scene.fields, start=2):
            commands.append(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasCommand(
                    text=f"{field.label}: {field.value}",
                    row=row,
                )
            )

        return HEOSApplicationRunOperationsDashboardRuntimeHistoryCanvasFrame(
            commands=tuple(commands),
        )
