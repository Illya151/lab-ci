from unittest.mock import Mock

import pytest

from shop.cart import Cart


def test_empty_cart(sample_cart: Cart) -> None:
    cart = Cart()
    assert cart.items_count() == 0
    assert cart.total() == 0.0


def test_add_item(sample_cart: Cart) -> None:
    assert sample_cart.items_count() == 6


def test_add_existing_item_increases_qty() -> None:
    cart = Cart()
    cart.add("book", price=100.0, qty=1)
    cart.add("book", price=100.0, qty=2)
    assert cart.items_count() == 3


@pytest.mark.parametrize(("price", "qty"), [(-1.0, 1), (100.0, 0), (100.0, -2)])
def test_add_invalid_arguments_raises(price: float, qty: int) -> None:
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add("item", price=price, qty=qty)


def test_remove_item(sample_cart: Cart) -> None:
    sample_cart.remove("pen")
    assert sample_cart.items_count() == 2


def test_remove_nonexistent_item_raises(sample_cart: Cart) -> None:
    with pytest.raises(KeyError):
        sample_cart.remove("laptop")


@pytest.mark.parametrize(
    ("discount", "expected"), [(0, 460.0), (10, 414.0), (50, 230.0), (100, 0.0)]
)
def test_total_with_discounts(sample_cart: Cart, discount: float, expected: float) -> None:
    assert sample_cart.total(discount_percent=discount) == pytest.approx(expected)


@pytest.mark.parametrize("invalid_discount", [-5.0, 105.0])
def test_total_invalid_discount_raises(sample_cart: Cart, invalid_discount: float) -> None:
    with pytest.raises(ValueError, match="discount_percent"):
        sample_cart.total(discount_percent=invalid_discount)


def test_total_in_currency(sample_cart: Cart) -> None:
    rates = Mock()
    rates.get_rate.return_value = 40.0
    assert sample_cart.total_in("USD", rates) == 11.5
    rates.get_rate.assert_called_once_with("USD")


def test_total_in_invalid_rate_raises(sample_cart: Cart) -> None:
    rates = Mock()
    rates.get_rate.return_value = 0.0
    with pytest.raises(ValueError, match="rate"):
        sample_cart.total_in("EUR", rates)


def test_most_expensive_item(sample_cart: Cart) -> None:
    item = sample_cart.most_expensive()
    assert item is not None
    assert item.name == "book"
    assert item.price == 200.0


def test_most_expensive_empty_cart() -> None:
    cart = Cart()
    assert cart.most_expensive() is None
