import pytest
from heos_ui.devices import Device, DeviceRegistry


def device(device_id: str = "fronius") -> Device:
    return Device(
        id=device_id,
        name=device_id.title(),
        device_type="energy",
    )


def test_registry_starts_empty() -> None:
    registry = DeviceRegistry()

    assert registry.count == 0
    assert registry.all() == ()


def test_register_device() -> None:
    registry = DeviceRegistry()

    registry.register(device())

    assert registry.count == 1
    assert registry.get("fronius") == device()


def test_duplicate_device_is_rejected() -> None:
    registry = DeviceRegistry()
    item = device()

    registry.register(item)

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(item)


def test_get_unknown_device() -> None:
    registry = DeviceRegistry()

    assert registry.get("missing") is None


def test_unregister_device() -> None:
    registry = DeviceRegistry()

    registry.register(device())
    registry.unregister("fronius")

    assert registry.count == 0
    assert registry.get("fronius") is None


def test_all_devices() -> None:
    registry = DeviceRegistry()

    registry.register(device("fronius"))
    registry.register(device("wattpilot"))

    assert tuple(item.id for item in registry.all()) == (
        "fronius",
        "wattpilot",
    )