import pytest
from heos_ui.theme.spacing import SPACING, SpacingTokens


def test_default_spacing_tokens_are_ordered() -> None:
    spacing = SpacingTokens()

    values = (
        spacing.none,
        spacing.xs,
        spacing.sm,
        spacing.md,
        spacing.lg,
        spacing.xl,
        spacing.xxl,
        spacing.huge,
    )

    assert values == tuple(sorted(values))
    assert len(values) == len(set(values))


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("none", 0),
        ("xs", 4),
        ("sm", 8),
        ("md", 12),
        ("lg", 16),
        ("xl", 24),
        ("xxl", 32),
        ("huge", 48),
    ],
)
def test_spacing_token_can_be_resolved(token: str, expected: int) -> None:
    assert SPACING.resolve(token) == expected


def test_unknown_spacing_token_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown spacing token"):
        SPACING.resolve("gigantic")


def test_spacing_tokens_are_immutable() -> None:
    spacing = SpacingTokens()

    with pytest.raises(AttributeError):
        spacing.md = 99  # type: ignore[misc]