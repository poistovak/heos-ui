from energy_value import EnergyUnit, EnergyValue


def test_default_format() -> None:
    value = EnergyValue(5.43, EnergyUnit.KILOWATT)

    assert value.formatted() == "5.4 kW"


def test_precision() -> None:
    value = EnergyValue(
        5.4321,
        EnergyUnit.KILOWATT,
        precision=2,
    )

    assert value.formatted() == "5.43 kW"


def test_percent() -> None:
    value = EnergyValue(
        82,
        EnergyUnit.PERCENT,
        precision=0,
    )

    assert value.formatted() == "82 %"


def test_voltage() -> None:
    value = EnergyValue(
        230,
        EnergyUnit.VOLT,
        precision=0,
    )

    assert value.formatted() == "230 V"