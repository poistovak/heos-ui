import pytest
from heos_ui.dashboard import Dashboard, DashboardRegistry


def test_registry_registers_and_returns_dashboard() -> None:
    registry = DashboardRegistry()
    dashboard = Dashboard(title="HEOS HOME")

    registry.register("home", dashboard)

    assert registry.get("home") is dashboard
    assert registry.exists("home")
    assert "home" in registry
    assert len(registry) == 1


def test_registry_lists_ids_and_dashboards() -> None:
    registry = DashboardRegistry()
    home = Dashboard(title="HEOS HOME")
    energy = Dashboard(title="ENERGY")

    registry.register("home", home)
    registry.register("energy", energy)

    assert registry.ids() == ("home", "energy")
    assert registry.all() == (home, energy)


def test_registry_rejects_duplicate_id() -> None:
    registry = DashboardRegistry()
    registry.register("home", Dashboard(title="HEOS HOME"))

    with pytest.raises(
        ValueError,
        match="Dashboard 'home' is already registered.",
    ):
        registry.register("home", Dashboard(title="OTHER"))


def test_registry_raises_for_unknown_dashboard() -> None:
    registry = DashboardRegistry()

    with pytest.raises(
        KeyError,
        match="Dashboard 'missing' is not registered.",
    ):
        registry.get("missing")


def test_registry_unregisters_dashboard() -> None:
    registry = DashboardRegistry()
    dashboard = Dashboard(title="HEOS HOME")
    registry.register("home", dashboard)

    removed = registry.unregister("home")

    assert removed is dashboard
    assert not registry.exists("home")
    assert len(registry) == 0


def test_registry_clear_removes_all_dashboards() -> None:
    registry = DashboardRegistry()
    registry.register("home", Dashboard(title="HEOS HOME"))
    registry.register("energy", Dashboard(title="ENERGY"))

    registry.clear()

    assert registry.ids() == ()
    assert registry.all() == ()
    assert len(registry) == 0