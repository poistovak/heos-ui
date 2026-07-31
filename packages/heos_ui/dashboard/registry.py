from __future__ import annotations

from .models import Dashboard


class DashboardRegistry:
    """Registry of dashboards identified by a unique ID."""

    def __init__(self) -> None:
        self._dashboards: dict[str, Dashboard] = {}

    def register(self, dashboard_id: str, dashboard: Dashboard) -> None:
        """Register a dashboard under a unique ID."""
        if dashboard_id in self._dashboards:
            raise ValueError(f"Dashboard '{dashboard_id}' is already registered.")

        self._dashboards[dashboard_id] = dashboard

    def get(self, dashboard_id: str) -> Dashboard:
        """Return a registered dashboard."""
        try:
            return self._dashboards[dashboard_id]
        except KeyError as error:
            raise KeyError(
                f"Dashboard '{dashboard_id}' is not registered."
            ) from error

    def exists(self, dashboard_id: str) -> bool:
        """Return whether a dashboard ID is registered."""
        return dashboard_id in self._dashboards

    def ids(self) -> tuple[str, ...]:
        """Return registered dashboard IDs."""
        return tuple(self._dashboards)

    def all(self) -> tuple[Dashboard, ...]:
        """Return all registered dashboards."""
        return tuple(self._dashboards.values())

    def unregister(self, dashboard_id: str) -> Dashboard:
        """Remove and return a registered dashboard."""
        try:
            return self._dashboards.pop(dashboard_id)
        except KeyError as error:
            raise KeyError(
                f"Dashboard '{dashboard_id}' is not registered."
            ) from error

    def clear(self) -> None:
        """Remove all registered dashboards."""
        self._dashboards.clear()

    def __len__(self) -> int:
        return len(self._dashboards)

    def __contains__(self, dashboard_id: object) -> bool:
        return dashboard_id in self._dashboards