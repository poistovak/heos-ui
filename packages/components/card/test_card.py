import pytest
from card import Card, CardPadding, CardVariant


def test_card_defaults() -> None:
    card = Card(
        title="Solar Production",
        content="5.4 kW",
    )

    assert card.title == "Solar Production"
    assert card.content == "5.4 kW"
    assert card.variant is CardVariant.DEFAULT
    assert card.padding is CardPadding.MEDIUM


def test_card_custom_configuration() -> None:
    card = Card(
        title="Battery",
        content="82%",
        variant=CardVariant.ELEVATED,
        padding=CardPadding.LARGE,
    )

    assert card.variant is CardVariant.ELEVATED
    assert card.padding is CardPadding.LARGE


def test_card_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title must not be empty"):
        Card(
            title=" ",
            content="5.4 kW",
        )


def test_card_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="content must not be empty"):
        Card(
            title="Solar Production",
            content=" ",
        )