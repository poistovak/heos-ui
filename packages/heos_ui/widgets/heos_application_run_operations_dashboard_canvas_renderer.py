from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_health_renderer import (
    HEOSApplicationRunOperationsDashboardRenderScene,
)
from .heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardCanvasCommand:
    kind: str
    text: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardCanvasFrame:
    commands: tuple[
        HEOSApplicationRunOperationsDashboardCanvasCommand,
        ...,
    ]
    severity: HEOSApplicationRunOperationsDashboardSeverity

    @property
    def command_count(self) -> int:
        return len(self.commands)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardCanvasRenderer:
    origin_x: int = 16
    origin_y: int = 16
    line_height: int = 28

    def render(
        self,
        scene: HEOSApplicationRunOperationsDashboardRenderScene,
    ) -> HEOSApplicationRunOperationsDashboardCanvasFrame:
        commands = [
            HEOSApplicationRunOperationsDashboardCanvasCommand(
                kind="title",
                text=scene.title,
                x=self.origin_x,
                y=self.origin_y,
            ),
            HEOSApplicationRunOperationsDashboardCanvasCommand(
                kind="status",
                text=scene.status,
                x=self.origin_x,
                y=self.origin_y + self.line_height,
            ),
        ]

        for index, field in enumerate(scene.fields):
            commands.append(
                HEOSApplicationRunOperationsDashboardCanvasCommand(
                    kind="field",
                    text=f"{field.label}: {field.value}",
                    x=self.origin_x,
                    y=(
                        self.origin_y
                        + self.line_height * (index + 2)
                    ),
                )
            )

        return HEOSApplicationRunOperationsDashboardCanvasFrame(
            commands=tuple(commands),
            severity=scene.severity,
        )
