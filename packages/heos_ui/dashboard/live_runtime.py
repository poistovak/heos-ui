from __future__ import annotations

from dataclasses import dataclass

from heos_ui.energy import (
    EnergyGraph,
    EnergyRenderer,
)
from heos_ui.energy.animation import AnimationEngine


@dataclass(slots=True)
class DashboardFrame:
    scene: object


class LiveDashboardRuntime:
    """Coordinates dashboard updates."""

    def __init__(
        self,
        graph: EnergyGraph,
        renderer: EnergyRenderer,
        animation: AnimationEngine,
    ) -> None:
        self._graph = graph
        self._renderer = renderer
        self._animation = animation

    @property
    def graph(self) -> EnergyGraph:
        return self._graph

    def render(self) -> DashboardFrame:
        scene = self._renderer.render(
            self._graph
        )

        return DashboardFrame(scene)