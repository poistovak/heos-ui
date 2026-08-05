from __future__ import annotations

from dataclasses import dataclass

from heos_ui.plugins import Plugin
from heos_ui.runtime.state_machine import RuntimeState

from .runtime import HEOSRuntime, create_runtime


@dataclass(slots=True)
class IntegrationRuntime:
    """High-level lifecycle and plugin integration for HEOS Core."""

    core: HEOSRuntime

    @classmethod
    def create(cls) -> IntegrationRuntime:
        return cls(
            core=create_runtime(),
        )

    @property
    def state(self) -> RuntimeState:
        return self.core.state_machine.state

    @property
    def running(self) -> bool:
        return self.state is RuntimeState.RUNNING

    def start(self) -> None:
        self.core.state_machine.start()
        self.core.logger.info("HEOS runtime started.")
        self.core.event_bus.publish(
            "runtime.started",
            self.state,
        )

    def pause(self) -> None:
        self.core.state_machine.pause()

        if self.state is RuntimeState.PAUSED:
            self.core.logger.info("HEOS runtime paused.")
            self.core.event_bus.publish(
                "runtime.paused",
                self.state,
            )

    def resume(self) -> None:
        self.core.state_machine.resume()

        if self.state is RuntimeState.RUNNING:
            self.core.logger.info("HEOS runtime resumed.")
            self.core.event_bus.publish(
                "runtime.resumed",
                self.state,
            )

    def stop(self) -> None:
        self.core.state_machine.stop()

        if self.state is RuntimeState.STOPPED:
            self.core.logger.info("HEOS runtime stopped.")
            self.core.event_bus.publish(
                "runtime.stopped",
                self.state,
            )

    def load_plugin(self, plugin: Plugin) -> None:
        self.core.plugins.load(plugin)
        self.core.logger.info(
            f"Plugin '{plugin.name}' loaded."
        )
        self.core.event_bus.publish(
            "plugin.loaded",
            plugin,
        )

    def unload_plugin(self, name: str) -> None:
        plugin = self.core.plugins.get(name)

        if plugin is None:
            return

        self.core.plugins.unload(name)
        self.core.logger.info(
            f"Plugin '{name}' unloaded."
        )
        self.core.event_bus.publish(
            "plugin.unloaded",
            plugin,
        )

    def tick(self, delta: float) -> None:
        if not self.running:
            return

        self.core.scheduler.tick(delta)