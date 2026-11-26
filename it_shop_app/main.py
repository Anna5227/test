from shop import (
    PRODUCTS,
    COUPONS,
    create_cart,
    add_to_cart,
    remove_from_cart,
    calculate_subtotal,
    checkout,
)


def print_line():
    print("=" * 48)


def show_products():
    print("\\n             КАТАЛОГ ТОВАРОВ")
    print_line()
    for product_id, product in PRODUCTS.items():
        availability = (
            f"В наличии: {product['stock']}"
            if product["stock"] > 0
            else "Нет в наличии"
        )
        print(
            f"{product_id}. {product['name']:<16} "
            f"{product['price']:>8,} руб. | {availability}"
        )
    print_line()


def show_cart(cart):
    print("\\n                 ВАША КОРЗИНА")
    print_line()

    if not cart:
        print("Корзина пока пуста.")
        print_line()
        return

    for product_id, quantity in cart.items():
        product = PRODUCTS[product_id]
        item_total = product["price"] * quantity
        print(
            f"{product['name']:<18} x {quantity:<3} "
            f"{item_total:>10,} руб."
        )

    print("-" * 48)
    print(f"Товары на сумму: {calculate_subtotal(cart):,} руб.")
    print_line()


def read_integer(prompt):
    value = input(prompt).strip()
    try:
        return int(value)
    except ValueError:
        print("Ошибка: введите целое число.")
        return None


def add_product_to_cart(cart):
    show_products()
    product_id = read_integer("Введите номер товара: ")
    if product_id is None:
        return

    quantity = read_integer("Введите количество: ")
    if quantity is None:
        return

    try:
        add_to_cart(cart, product_id, quantity)
        print("Товар добавлен в корзину.")
    except (KeyError, ValueError) as error:
        print(f"Не удалось добавить товар: {error}")


def remove_product_from_cart(cart):
    show_cart(cart)
    if not cart:
        return

    product_id = read_integer("Введите номер товара для удаления: ")
    if product_id is None:
        return

    quantity = read_integer("Сколько единиц удалить: ")
    if quantity is None:
        return

    try:
        remove_from_cart(cart, product_id, quantity)
        print("Корзина обновлена.")
    except (KeyError, ValueError) as error:
        print(f"Не удалось изменить корзину: {error}")


def make_checkout(cart):
    if not cart:
        print("Сначала добавьте товары в корзину.")
        return

    print("\\n             ОФОРМЛЕНИЕ ЗАКАЗА")
    print_line()

    customer = {
        "name": input("Ваше имя: ").strip(),
        "email": input("Email: ").strip(),
        "phone": input("Телефон: ").strip(),
    }

    coupon = input("Промокод (Enter — без промокода): ").strip().upper()
    if not coupon:
        coupon = None

    print("\\nСпособ доставки:")
    print("1. Стандартная")
    print("2. Экспресс")
    delivery_choice = input("Выберите вариант: ").strip()

    delivery_types = {"1": "standard", "2": "express"}
    delivery_type = delivery_types.get(delivery_choice)

    if delivery_type is None:
        print("Неизвестный способ доставки.")
        return

    try:
        order = checkout(customer, cart, coupon, delivery_type)
    except (KeyError, ValueError) as error:
        print(f"Не удалось оформить заказ: {error}")
        return

    print("\\n             ЗАКАЗ ОФОРМЛЕН")
    print_line()
    print(f"Покупатель:          {order['customer']}")
    print(f"Стоимость товаров:   {order['subtotal']:,.2f} руб.")
    print(f"Доставка:            {order['delivery']:,.2f} руб.")
    print("-" * 48)
    print(f"ИТОГО:               {order['total']:,.2f} руб.")
    print(f"Статус:              {order['status']}")
    print_line()

    cart.clear()


def main():
    cart = create_cart()

    while True:
        print("\\n")
        print_line()
        print("                  IT-SHOP")
        print_line()
        print("1. Посмотреть каталог")
        print("2. Добавить товар в корзину")
        print("3. Удалить товар из корзины")
        print("4. Посмотреть корзину")
        print("5. Оформить заказ")
        print("0. Выход")
        print_line()

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_products()
        elif choice == "2":
            add_product_to_cart(cart)
        elif choice == "3":
            remove_product_from_cart(cart)
        elif choice == "4":
            show_cart(cart)
        elif choice == "5":
            make_checkout(cart)
        elif choice == "0":
            print("Спасибо за покупку! До свидания.")
            break
        else:
            print("Такого пункта меню нет. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
