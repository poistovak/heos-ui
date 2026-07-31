import pytest
from badge import Badge, BadgeVariant


def test_badge_defaults() -> None:
    badge = Badge(label="Online")

    assert badge.label == "Online"
    assert badge.variant is BadgeVariant.INFO


def test_badge_variant() -> None:
    badge = Badge(label="Charging", variant=BadgeVariant.SUCCESS)

    assert badge.variant is BadgeVariant.SUCCESS


def test_badge_rejects_empty_label() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        Badge(label=" ")