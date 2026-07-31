from battery_indicator import BatteryIndicator, BatteryState


def test_percentage() -> None:
    battery = BatteryIndicator(
        soc=82,
        state=BatteryState.CHARGING,
    )

    assert battery.percentage() == "82%"


def test_label() -> None:
    battery = BatteryIndicator(
        soc=82,
        state=BatteryState.DISCHARGING,
    )

    assert battery.label() == "Discharging"


def test_low_false() -> None:
    battery = BatteryIndicator(
        soc=45,
        state=BatteryState.IDLE,
    )

    assert battery.is_low() is False


def test_low_true() -> None:
    battery = BatteryIndicator(
        soc=15,
        state=BatteryState.CRITICAL,
    )

    assert battery.is_low() is True