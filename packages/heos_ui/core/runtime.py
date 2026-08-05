from __future__ import annotations

from dataclasses import dataclass

from heos_ui.capabilities import CapabilityRegistry
from heos_ui.config import ConfigurationService
from heos_ui.devices import DeviceRegistry
from heos_ui.diagnostics import (
    DiagnosticsEngine,
    HealthMonitor,
)
from heos_ui.events.bus import EventBus
from heos_ui.logging import Logger
from heos_ui.plugins import PluginManager
from heos_ui.runtime.scheduler_core import Scheduler
from heos_ui.runtime.state_machine import RuntimeStateMachine
from heos_ui.services import ServiceRegistry
from heos_ui.telemetry import TelemetryService


@dataclass(slots=True)
class HEOSRuntime:
    configuration: ConfigurationService
    devices: DeviceRegistry
    capabilities: CapabilityRegistry
    services: ServiceRegistry
    plugins: PluginManager
    event_bus: EventBus
    scheduler: Scheduler
    state_machine: RuntimeStateMachine
    telemetry: TelemetryService
    diagnostics: DiagnosticsEngine
    health: HealthMonitor
    logger: Logger


def create_runtime() -> HEOSRuntime:
    telemetry = TelemetryService()
    diagnostics = DiagnosticsEngine()
    event_bus = EventBus()

    return HEOSRuntime(
        configuration=ConfigurationService(),
        devices=DeviceRegistry(),
        capabilities=CapabilityRegistry(),
        services=ServiceRegistry(),
        plugins=PluginManager(),
        event_bus=event_bus,
        scheduler=Scheduler(),
        state_machine=RuntimeStateMachine(),
        telemetry=telemetry,
        diagnostics=diagnostics,
        health=HealthMonitor(
            diagnostics=diagnostics,
            telemetry=telemetry,
            event_bus=event_bus,
        ),
        logger=Logger("runtime"),
    )