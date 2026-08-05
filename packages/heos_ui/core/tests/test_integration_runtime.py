from heos_ui.core import IntegrationRuntime
from heos_ui.plugins import Plugin
from heos_ui.runtime.state_machine import RuntimeState


def test_create_runtime() -> None:
    runtime = IntegrationRuntime.create()

    assert runtime.state is RuntimeState.CREATED
    assert not runtime.running


def test_start_runtime() -> None:
    runtime = IntegrationRuntime.create()

    runtime.start()

    assert runtime.running
    assert runtime.state is RuntimeState.RUNNING


def test_pause_and_resume_runtime() -> None:
    runtime = IntegrationRuntime.create()

    runtime.start()
    runtime.pause()

    assert runtime.state is RuntimeState.PAUSED

    runtime.resume()

    assert runtime.running


def test_stop_runtime() -> None:
    runtime = IntegrationRuntime.create()

    runtime.start()
    runtime.stop()

    assert runtime.state is RuntimeState.STOPPED
    assert not runtime.running


def test_load_plugin() -> None:
    runtime = IntegrationRuntime.create()
    plugin = Plugin(
        name="fronius",
        version="1.0.0",
    )

    runtime.load_plugin(plugin)

    assert runtime.core.plugins.get("fronius") == plugin


def test_unload_plugin() -> None:
    runtime = IntegrationRuntime.create()

    runtime.load_plugin(
        Plugin(name="wattpilot")
    )
    runtime.unload_plugin("wattpilot")

    assert runtime.core.plugins.get("wattpilot") is None


def test_plugin_event_is_published() -> None:
    runtime = IntegrationRuntime.create()
    received = []

    runtime.core.event_bus.subscribe(
        "plugin.loaded",
        received.append,
    )

    plugin = Plugin(name="home_assistant")
    runtime.load_plugin(plugin)

    assert received == [plugin]


def test_tick_runs_scheduler_only_while_running() -> None:
    runtime = IntegrationRuntime.create()
    calls = []

    runtime.core.scheduler.every(
        1.0,
        lambda: calls.append("tick"),
    )

    runtime.tick(1.0)

    assert calls == []

    runtime.start()
    runtime.tick(1.0)

    assert calls == ["tick"]


def test_lifecycle_is_logged() -> None:
    runtime = IntegrationRuntime.create()

    runtime.start()
    runtime.stop()

    assert runtime.core.logger.count == 2