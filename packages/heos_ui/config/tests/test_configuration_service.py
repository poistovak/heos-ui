import pytest
from heos_ui.config import ConfigurationService


def test_starts_empty() -> None:
    config = ConfigurationService()

    assert config.count == 0
    assert config.snapshot() == {}


def test_set_and_get() -> None:
    config = ConfigurationService()

    config.set(
        "ui.theme",
        "dark",
    )

    assert config.get("ui.theme") == "dark"
    assert config.has("ui.theme")


def test_get_default() -> None:
    config = ConfigurationService()

    assert config.get(
        "missing",
        25,
    ) == 25


def test_require() -> None:
    config = ConfigurationService()

    config.set(
        "fronius.host",
        "192.168.50.163",
    )

    assert config.require(
        "fronius.host"
    ) == "192.168.50.163"


def test_require_missing() -> None:
    config = ConfigurationService()

    with pytest.raises(
        KeyError,
        match="missing",
    ):
        config.require("missing")


def test_empty_key_is_rejected() -> None:
    config = ConfigurationService()

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        config.set(
            "",
            "value",
        )


def test_remove() -> None:
    config = ConfigurationService()

    config.set(
        "wattpilot.max_current",
        16,
    )

    assert config.remove(
        "wattpilot.max_current"
    )
    assert not config.has(
        "wattpilot.max_current"
    )
    assert not config.remove(
        "wattpilot.max_current"
    )


def test_update_multiple_values() -> None:
    config = ConfigurationService()

    config.update(
        {
            "ui.theme": "dark",
            "fronius.host": "192.168.50.163",
            "wattpilot.max_current": 16,
        }
    )

    assert config.count == 3


def test_snapshot_is_copy() -> None:
    config = ConfigurationService()

    config.set(
        "ui.theme",
        "dark",
    )

    snapshot = config.snapshot()
    snapshot.clear()

    assert config.count == 1


def test_clear() -> None:
    config = ConfigurationService()

    config.set(
        "ui.theme",
        "dark",
    )
    config.clear()

    assert config.count == 0