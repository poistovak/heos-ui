from __future__ import annotations

from dataclasses import dataclass

from .brain_presenter import (
    BrainStatusPresentation,
    BrainStatusSeverity,
)


@dataclass(slots=True, frozen=True)
class BrainRenderField:
    label: str
    value: str


@dataclass(slots=True, frozen=True)
class BrainRenderScene:
    title: str
    status: str
    health: str
    severity: BrainStatusSeverity
    fields: tuple[BrainRenderField, ...]


class BrainStatusRenderer:
    """Transforms brain presentation into a renderable scene."""

    def render(
        self,
        presentation: BrainStatusPresentation,
    ) -> BrainRenderScene:
        fields = (
            BrainRenderField(
                label="Cycle",
                value=presentation.cycle,
            ),
            BrainRenderField(
                label="Execution",
                value=presentation.execution,
            ),
            BrainRenderField(
                label="Targets",
                value=presentation.targets,
            ),
        )

        return BrainRenderScene(
            title=presentation.title,
            status=presentation.status,
            health=presentation.health,
            severity=presentation.severity,
            fields=fields,
        )