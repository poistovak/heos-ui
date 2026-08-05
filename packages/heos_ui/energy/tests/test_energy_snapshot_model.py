import pytest
from heos_ui.energy import EnergySnapshot


def test_default_snapshot() -> None:
    snapshot = EnergySnapshot()

    assert snapshot.pv_power == 0.0
    assert snapshot.house_power == 0.0
    assert snapshot.surplus_power == 0.0
    assert snapshot.battery_soc is None


def test_surplus_power() -> None:
    snapshot = EnergySnapshot(
        pv_power=6500.0,
        house_power=2500.0,
    )

    assert snapshot.surplus_power == 4000.0


def test_surplus_never_becomes_negative() -> None:
    snapshot = EnergySnapshot(
        pv_power=1000.0,
        house_power=3000.0,
    )

    assert snapshot.surplus_power == 0.0


def test_grid_import_and_export() -> None:
    importing = EnergySnapshot(
        grid_power=1800.0,
    )
    exporting = EnergySnapshot(
        grid_power=-2400.0,
    )

    assert importing.grid_import_power == 1800.0
    assert importing.grid_export_power == 0.0

    assert exporting.grid_import_power == 0.0
    assert exporting.grid_export_power == 2400.0


def test_battery_direction() -> None:
    charging = EnergySnapshot(
        battery_power=2200.0,
        battery_online=True,
    )
    discharging = EnergySnapshot(
        battery_power=-1500.0,
        battery_online=True,
    )

    assert charging.battery_charging
    assert not charging.battery_discharging

    assert discharging.battery_discharging
    assert not discharging.battery_charging


def test_invalid_battery_soc_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="between 0 and 100",
    ):
        EnergySnapshot(
            battery_soc=101.0,
        )


def test_negative_device_power_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="ev_power",
    ):
        EnergySnapshot(
            ev_power=-1.0,
        )