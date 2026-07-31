from heos_ui.state import StateStore


def test_state_store_set_and_get() -> None:
    store = StateStore()

    store.set("pv_power", 8.4)
    store.set("battery_soc", 83)

    assert store.get("pv_power") == 8.4
    assert store.get("battery_soc") == 83
    assert len(store) == 2


def test_state_store_default_value() -> None:
    store = StateStore()

    assert store.get("missing", 0) == 0


def test_state_store_remove_and_clear() -> None:
    store = StateStore()

    store.set("house_power", 2.7)
    assert "house_power" in store

    store.remove("house_power")
    assert "house_power" not in store

    store.set("grid_mode", "export")
    store.clear()

    assert len(store) == 0