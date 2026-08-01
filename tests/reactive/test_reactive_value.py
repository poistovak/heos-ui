from heos_ui.reactive import ReactiveValue


def test_set_notifies_subscriber_after_change() -> None:
    value = ReactiveValue(10)
    received: list[int] = []

    value.subscribe(received.append)

    changed = value.set(20)

    assert changed is True
    assert value.value == 20
    assert received == [20]


def test_set_does_not_notify_when_value_is_unchanged() -> None:
    value = ReactiveValue(10)
    received: list[int] = []

    value.subscribe(received.append)

    changed = value.set(10)

    assert changed is False
    assert received == []


def test_subscribers_are_called_in_registration_order() -> None:
    value = ReactiveValue("created")
    calls: list[str] = []

    value.subscribe(lambda current: calls.append(f"first:{current}"))
    value.subscribe(lambda current: calls.append(f"second:{current}"))

    value.set("visible")

    assert calls == [
        "first:visible",
        "second:visible",
    ]


def test_subscription_can_be_cancelled() -> None:
    value = ReactiveValue(10)
    received: list[int] = []

    subscription = value.subscribe(received.append)
    subscription.unsubscribe()

    value.set(20)

    assert received == []
    assert subscription.active is False


def test_unsubscribe_is_idempotent() -> None:
    value = ReactiveValue(10)

    subscription = value.subscribe(lambda _: None)

    subscription.unsubscribe()
    subscription.unsubscribe()

    assert value.subscriber_count == 0


def test_subscriber_can_unsubscribe_during_notification() -> None:
    value = ReactiveValue(10)
    received: list[int] = []

    subscription = None

    def subscriber(current: int) -> None:
        received.append(current)
        assert subscription is not None
        subscription.unsubscribe()

    subscription = value.subscribe(subscriber)

    value.set(20)
    value.set(30)

    assert received == [20]


def test_notify_immediately_receives_current_value() -> None:
    value = ReactiveValue(10)
    received: list[int] = []

    value.subscribe(received.append, notify_immediately=True)

    assert received == [10]