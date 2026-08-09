from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_health_renderer import (
    HEOSApplicationRunOperationsRenderScene,
)
from .heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsCanvasCommand:
    kind: str
    text: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsCanvasFrame:
    commands: tuple[HEOSApplicationRunOperationsCanvasCommand, ...]
    severity: HEOSApplicationRunOperationsSeverity

    @property
    def command_count(self) -> int:
        return len(self.commands)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsCanvasRenderer:
    origin_x: int = 16
    origin_y: int = 16
    line_height: int = 28

    def render(
        self,
        scene: HEOSApplicationRunOperationsRenderScene,
    ) -> HEOSApplicationRunOperationsCanvasFrame:
        commands: list[HEOSApplicationRunOperationsCanvasCommand] = [
            HEOSApplicationRunOperationsCanvasCommand(
                kind="title",
                text=scene.title,
                x=self.origin_x,
                y=self.origin_y,
            ),
            HEOSApplicationRunOperationsCanvasCommand(
                kind="status",
                text=scene.status,
                x=self.origin_x,
                y=self.origin_y + self.line_height,
            ),
        ]

        for index, field in enumerate(scene.fields):
            commands.append(
                HEOSApplicationRunOperationsCanvasCommand(
                    kind="field",
                    text=f"{field.label}: {field.value}",
                    x=self.origin_x,
                    y=self.origin_y
                    + self.line_height * (index + 2),
                )
            )

        return HEOSApplicationRunOperationsCanvasFrame(
            commands=tuple(commands),
            severity=scene.severity,
        )
