import pytest
from src.checkout import Checkout


def test_single_item_no_discounts():
    checkout = Checkout(tax_rate=0.18)
    checkout.add_item(price=100.0, quantity=1)
    total = checkout.calculate_total(is_subscriber=False)

    assert total == 118.0

def test_multiple_items_with_bundle_discount():
    checkout = Checkout(tax_rate=0.18)
    checkout.add_item(price=50.0, quantity=2, is_bundle=True)   # bundle
    checkout.add_item(price=40.0, quantity=1, is_bundle=False)  # normal

    subtotal = 50 * 2 + 40  # 140
    discounted = subtotal * (1 - checkout.bundle_discount)  # 140 * 0.85 = 119
    expected_total = round(discounted + discounted * 0.18, 2)

    total = checkout.calculate_total(is_subscriber=False)
    assert total == expected_total


def test_subscription_discount_applied():
    checkout = Checkout(tax_rate=0.18)
    checkout.add_item(price=100.0, quantity=1)

    subtotal = 100
    after_sub_discount = subtotal * (1 - checkout.subscription_discount)  # 90
    expected_total = round(after_sub_discount + after_sub_discount * 0.18, 2)

    total = checkout.calculate_total(is_subscriber=True)
    assert total == expected_total


def test_subscription_and_bundle_together():
    checkout = Checkout(tax_rate=0.18)
    checkout.add_item(price=80.0, quantity=1, is_bundle=True)

    subtotal = 80
    after_bundle = subtotal * (1 - checkout.bundle_discount)
    after_sub = after_bundle * (1 - checkout.subscription_discount)
    expected_total = round(after_sub + after_sub * 0.18, 2)

    total = checkout.calculate_total(is_subscriber=True)
    assert total == expected_total


@pytest.mark.parametrize(
    "items,is_subscriber",
    [
        ([(10, 1, False)], False),
        ([(10, 2, True)], True),
        ([(5, 3, False), (20, 1, True)], True),
    ],
)
def test_no_negative_totals(items, is_subscriber):
    checkout = Checkout()
    for price, quantity, is_bundle in items:
        checkout.add_item(price=price, quantity=quantity, is_bundle=is_bundle)

    total = checkout.calculate_total(is_subscriber=is_subscriber)
    assert total >= 0
