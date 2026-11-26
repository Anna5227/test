import pytest

from shop import (
    PRODUCTS,
    add_to_cart,
    apply_coupon,
    calculate_delivery,
    calculate_subtotal,
    checkout,
    create_cart,
    find_product,
    remove_from_cart,
    validate_customer,
)


@pytest.fixture
def valid_customer():
    return {
        "name": "Иван Иванов",
        "email": "ivan@example.com",
        "phone": "+7 (999) 123-45-67",
    }


@pytest.fixture
def empty_cart():
    return create_cart()

@pytest.mark.parametrize("product_id", [1, 2, 3, 4, 5])
def test_find_product_existing(product_id):
    assert find_product(product_id) == PRODUCTS[product_id]


@pytest.mark.parametrize("product_id", [0, 6, 999, "1"])
def test_find_product_missing(product_id):
    with pytest.raises(KeyError, match="Товар не найден"):
        find_product(product_id)

def test_create_cart_returns_new_empty_dict():
    cart = create_cart()

    assert cart == {}
    assert isinstance(cart, dict)

    cart[1] = 1
    assert create_cart() == {}

def test_add_to_cart_adds_product(empty_cart):
    result = add_to_cart(empty_cart, 1, 2)

    assert result is empty_cart
    assert empty_cart == {1: 2}


def test_add_to_cart_increments_quantity(empty_cart):
    add_to_cart(empty_cart, 1, 2)
    add_to_cart(empty_cart, 1, 1)

    assert empty_cart == {1: 3}


def test_add_to_cart_adds_different_products(empty_cart):
    add_to_cart(empty_cart, 1, 1)
    add_to_cart(empty_cart, 2, 5)

    assert empty_cart == {1: 1, 2: 5}


@pytest.mark.parametrize("quantity", [0, -1, -10, 1.5, "2", None])
def test_add_to_cart_rejects_invalid_quantity(empty_cart, quantity):
    with pytest.raises(
        ValueError,
        match="Количество должно быть положительным целым числом",
    ):
        add_to_cart(empty_cart, 1, quantity)


def test_add_to_cart_rejects_quantity_over_stock(empty_cart):
    with pytest.raises(ValueError, match="Недостаточно товара на складе"):
        add_to_cart(empty_cart, 1, PRODUCTS[1]["stock"] + 1)


def test_add_to_cart_rejects_quantity_over_stock_with_existing(empty_cart):
    add_to_cart(empty_cart, 1, 3)

    with pytest.raises(ValueError, match="Недостаточно товара на складе"):
        add_to_cart(empty_cart, 1, 3)


def test_add_to_cart_rejects_missing_product(empty_cart):
    with pytest.raises(KeyError, match="Товар не найден"):
        add_to_cart(empty_cart, 999, 1)

def test_remove_from_cart_decreases_quantity(empty_cart):
    add_to_cart(empty_cart, 1, 3)

    result = remove_from_cart(empty_cart, 1, 1)

    assert result is empty_cart
    assert empty_cart == {1: 2}


def test_remove_from_cart_removes_item(empty_cart):
    add_to_cart(empty_cart, 2, 5)

    remove_from_cart(empty_cart, 2, 5)

    assert empty_cart == {}


def test_remove_from_cart_removes_item_if_quantity_greater(empty_cart):
    add_to_cart(empty_cart, 2, 3)

    remove_from_cart(empty_cart, 2, 10)

    assert empty_cart == {}


def test_remove_from_cart_rejects_missing_product(empty_cart):
    with pytest.raises(KeyError, match="Товара нет в корзине"):
        remove_from_cart(empty_cart, 1, 1)


@pytest.mark.parametrize("quantity", [0, -1, -10, 1.5, "2", None])
def test_remove_from_cart_rejects_invalid_quantity(empty_cart, quantity):
    add_to_cart(empty_cart, 1, 2)

    with pytest.raises(
        ValueError,
        match="Количество должно быть положительным целым числом",
    ):
        remove_from_cart(empty_cart, 1, quantity)

@pytest.mark.parametrize(
    "cart, expected",
    [
        ({}, 0),
        ({1: 1}, 75000),
        ({2: 3}, 4500),
        ({1: 1, 2: 2}, 78000),
        ({1: 1, 2: 2, 3: 1}, 81500),
    ],
)
def test_calculate_subtotal(cart, expected):
    assert calculate_subtotal(cart) == expected


@pytest.mark.parametrize("quantity", [0, -1, 1.5, "2"])
def test_calculate_subtotal_rejects_invalid_quantity(quantity):
    with pytest.raises(
        ValueError,
        match="Некорректное количество товара в корзине",
    ):
        calculate_subtotal({1: quantity})


def test_calculate_subtotal_rejects_unknown_product():
    with pytest.raises(KeyError, match="Товар не найден"):
        calculate_subtotal({999: 1})

@pytest.mark.parametrize(
    "total, coupon, expected",
    [
        (1000, "SALE10", 900.0),
        (1000, "SALE20", 800.0),
        (2500, "SALE10", 2250.0),
        (0, "SALE20", 0.0),
    ],
)
def test_apply_coupon(total, coupon, expected):
    assert apply_coupon(total, coupon) == pytest.approx(expected)


def test_apply_coupon_rejects_unknown_coupon():
    with pytest.raises(ValueError, match="Недействительный промокод"):
        apply_coupon(1000, "NOPE")


def test_apply_coupon_rejects_negative_total():
    with pytest.raises(
        ValueError,
        match="Сумма заказа не может быть отрицательной",
    ):
        apply_coupon(-1, "SALE10")

@pytest.mark.parametrize(
    "total, delivery_type, expected",
    [
        (1000, "standard", 300),
        (1000, "express", 700),
        (4999, "standard", 300),
        (4999, "express", 700),
        (5000, "standard", 0),
        (5000, "express", 0),
        (75000, "express", 0),
    ],
)
def test_calculate_delivery(total, delivery_type, expected):
    assert calculate_delivery(total, delivery_type) == expected


def test_calculate_delivery_rejects_unknown_type():
    with pytest.raises(ValueError, match="Неизвестный способ доставки"):
        calculate_delivery(1000, "pickup")


def test_calculate_delivery_rejects_negative_total():
    with pytest.raises(
        ValueError,
        match="Сумма заказа не может быть отрицательной",
    ):
        calculate_delivery(-1, "standard")

def test_validate_customer_accepts_valid_data(valid_customer):
    assert validate_customer(valid_customer) is True


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("name", "", "Не указано имя"),
        ("name", "   ", "Не указано имя"),
        ("email", "invalid", "Некорректный email"),
        ("email", "user@example", "Некорректный email"),
        ("phone", "12345", "Некорректный телефон"),
        ("phone", "", "Некорректный телефон"),
    ],
)
def test_validate_customer_rejects_invalid_fields(
    valid_customer,
    field,
    value,
    message,
):
    customer = valid_customer.copy()
    customer[field] = value

    with pytest.raises(ValueError, match=message):
        validate_customer(customer)


def test_validate_customer_rejects_missing_name(valid_customer):
    customer = valid_customer.copy()
    del customer["name"]

    with pytest.raises(ValueError, match="Не указано имя"):
        validate_customer(customer)

def test_checkout_success(valid_customer):
    cart = create_cart()
    add_to_cart(cart, 1, 1)

    order = checkout(valid_customer, cart)

    assert order == {
        "customer": "Иван Иванов",
        "subtotal": 75000,
        "delivery": 0,
        "total": 75000,
        "status": "created",
    }


def test_checkout_strips_customer_name(valid_customer):
    customer = valid_customer.copy()
    customer["name"] = "  Иван Иванов  "

    cart = create_cart()
    add_to_cart(cart, 1, 1)

    order = checkout(customer, cart)

    assert order["customer"] == "Иван Иванов"


def test_checkout_with_coupon(valid_customer):
    cart = create_cart()
    add_to_cart(cart, 1, 1)

    order = checkout(valid_customer, cart, coupon="SALE10")

    assert order["subtotal"] == pytest.approx(67500.0)
    assert order["delivery"] == 0
    assert order["total"] == pytest.approx(67500.0)
    assert order["status"] == "created"


def test_checkout_with_express_delivery(valid_customer):
    cart = create_cart()
    add_to_cart(cart, 2, 1)

    order = checkout(valid_customer, cart, delivery_type="express")

    assert order["subtotal"] == 1500
    assert order["delivery"] == 700
    assert order["total"] == 2200


def test_checkout_rejects_empty_cart(valid_customer):
    with pytest.raises(ValueError, match="Корзина пуста"):
        checkout(valid_customer, create_cart())


def test_checkout_rejects_invalid_customer():
    cart = {1: 1}
    customer = {"name": "", "email": "bad", "phone": "1"}

    with pytest.raises(ValueError, match="Не указано имя"):
        checkout(customer, cart)


def test_checkout_rejects_invalid_coupon(valid_customer):
    cart = {1: 1}

    with pytest.raises(ValueError, match="Недействительный промокод"):
        checkout(valid_customer, cart, coupon="BAD")


def test_checkout_rejects_unknown_delivery_type(valid_customer):
    cart = {2: 1}

    with pytest.raises(ValueError, match="Неизвестный способ доставки"):
        checkout(valid_customer, cart, delivery_type="pickup")