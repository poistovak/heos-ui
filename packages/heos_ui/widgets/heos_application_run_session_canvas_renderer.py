from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_session_health_renderer import (
    HEOSApplicationRunSessionRenderScene,
)
from .heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionCanvasCommand:
    kind: str
    text: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionCanvasFrame:
    commands: tuple[HEOSApplicationRunSessionCanvasCommand, ...]
    severity: HEOSApplicationRunSessionSeverity

    @property
    def command_count(self) -> int:
        return len(self.commands)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionCanvasRenderer:
    origin_x: int = 16
    origin_y: int = 16
    line_height: int = 28

    def render(
        self,
        scene: HEOSApplicationRunSessionRenderScene,
    ) -> HEOSApplicationRunSessionCanvasFrame:
        commands: list[HEOSApplicationRunSessionCanvasCommand] = [
            HEOSApplicationRunSessionCanvasCommand(
                kind="title",
                text=scene.title,
                x=self.origin_x,
                y=self.origin_y,
            ),
            HEOSApplicationRunSessionCanvasCommand(
                kind="status",
                text=scene.status,
                x=self.origin_x,
                y=self.origin_y + self.line_height,
            ),
        ]

        for index, field in enumerate(scene.fields):
            commands.append(
                HEOSApplicationRunSessionCanvasCommand(
                    kind="field",
                    text=f"{field.label}: {field.value}",
                    x=self.origin_x,
                    y=self.origin_y
                    + self.line_height * (index + 2),
                )
            )

        return HEOSApplicationRunSessionCanvasFrame(
            commands=tuple(commands),
            severity=scene.severity,
        )
