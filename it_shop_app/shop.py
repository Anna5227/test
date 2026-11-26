PRODUCTS = {
    1: {"name": "Ноутбук", "price": 75000, "stock": 5},
    2: {"name": "Мышь", "price": 1500, "stock": 20},
    3: {"name": "Клавиатура", "price": 3500, "stock": 10},
    4: {"name": "Монитор", "price": 25000, "stock": 0},
    5: {"name": "Наушники", "price": 4500, "stock": 8},
}

COUPONS = {
    "SALE10": 10,
    "SALE20": 20,
}


def find_product(product_id):
    if product_id not in PRODUCTS:
        raise KeyError("Товар не найден")
    return PRODUCTS[product_id]


def create_cart():
    return {}


def add_to_cart(cart, product_id, quantity):
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Количество должно быть положительным целым числом")

    product = find_product(product_id)
    current_quantity = cart.get(product_id, 0)

    if current_quantity + quantity > product["stock"]:
        raise ValueError("Недостаточно товара на складе")

    cart[product_id] = current_quantity + quantity
    return cart


def remove_from_cart(cart, product_id, quantity):
    if product_id not in cart:
        raise KeyError("Товара нет в корзине")

    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Количество должно быть положительным целым числом")

    if quantity >= cart[product_id]:
        del cart[product_id]
    else:
        cart[product_id] -= quantity

    return cart


def calculate_subtotal(cart):
    total = 0

    for product_id, quantity in cart.items():
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Некорректное количество товара в корзине")

        product = find_product(product_id)
        total += product["price"] * quantity

    return total


def apply_coupon(total, coupon):
    if total < 0:
        raise ValueError("Сумма заказа не может быть отрицательной")

    if coupon not in COUPONS:
        raise ValueError("Недействительный промокод")

    discount = COUPONS[coupon]
    return total - (total * discount / 100)


def calculate_delivery(total, delivery_type):
    if total < 0:
        raise ValueError("Сумма заказа не может быть отрицательной")

    if delivery_type not in ("standard", "express"):
        raise ValueError("Неизвестный способ доставки")

    if total >= 5000:
        return 0

    if delivery_type == "express":
        return 700

    return 300


def validate_customer(customer):
    if not customer.get("name", "").strip():
        raise ValueError("Не указано имя")

    email = customer.get("email", "")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Некорректный email")

    phone = customer.get("phone", "")
    digits = "".join(char for char in phone if char.isdigit())
    if len(digits) < 10:
        raise ValueError("Некорректный телефон")

    return True


def checkout(customer, cart, coupon=None, delivery_type="standard"):
    validate_customer(customer)

    if not cart:
        raise ValueError("Корзина пуста")

    subtotal = calculate_subtotal(cart)

    if coupon:
        subtotal = apply_coupon(subtotal, coupon)

    delivery = calculate_delivery(subtotal, delivery_type)

    return {
        "customer": customer["name"].strip(),
        "subtotal": subtotal,
        "delivery": delivery,
        "total": subtotal + delivery,
        "status": "created",
    }
