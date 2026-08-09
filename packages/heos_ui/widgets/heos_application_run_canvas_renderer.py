from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_presenter import HEOSApplicationRunSeverity
from .heos_application_run_status_renderer import (
    HEOSApplicationRunRenderScene,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunCanvasCommand:
    kind: str
    text: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunCanvasFrame:
    commands: tuple[HEOSApplicationRunCanvasCommand, ...]
    severity: HEOSApplicationRunSeverity

    @property
    def command_count(self) -> int:
        return len(self.commands)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunCanvasRenderer:
    origin_x: int = 16
    origin_y: int = 16
    line_height: int = 28

    def render(
        self,
        scene: HEOSApplicationRunRenderScene,
    ) -> HEOSApplicationRunCanvasFrame:
        commands: list[HEOSApplicationRunCanvasCommand] = [
            HEOSApplicationRunCanvasCommand(
                kind="title",
                text=scene.title,
                x=self.origin_x,
                y=self.origin_y,
            ),
            HEOSApplicationRunCanvasCommand(
                kind="status",
                text=scene.status,
                x=self.origin_x,
                y=self.origin_y + self.line_height,
            ),
        ]

        for index, field in enumerate(scene.fields):
            commands.append(
                HEOSApplicationRunCanvasCommand(
                    kind="field",
                    text=f"{field.label}: {field.value}",
                    x=self.origin_x,
                    y=self.origin_y + self.line_height * (index + 2),
                )
            )

        return HEOSApplicationRunCanvasFrame(
            commands=tuple(commands),
            severity=scene.severity,
        )
