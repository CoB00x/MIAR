import requests

URL = "http://localhost:8002/api"


def component_tests():
    # Получить меню
    print("Тест1: Получение меню")
    response = requests.get(f"{URL}/menu")
    assert response.status_code == 200, "Не удалось получить меню"
    menu = response.json()
    print('\tМеню получено. Категории: ', [key for key in menu.get('categories')])

    # Создание заказа
    print("Тест2: Создание заказа")
    first_item = list(menu['categories'].values())[0][0]
    order_data = {
        "guest_id": "test-user-123",
        "room_number": "101",
        "order_type": "room_service",
        "items": [{"menu_item_id": first_item["id"], "quantity": 1}]
    }
    response = requests.post(f"{URL}/orders", json=order_data)
    assert response.status_code == 200, "Не удалось создать заказ"
    order = response.json()
    print("\tЗаказ создан. ID заказа: {order['order_id']}")

    # Получение заказа
    print("Тест3: Получение заакза")
    response = requests.get(f"{URL}/orders/{order['order_id']}")
    assert response.status_code == 200, "Не удалось получить заказ"
    print("\tЗаказ найден:", response.json())

    # Бронирование столика
    print("Тест4: Бронирование столика")
    reservation_data = {
        "guest_id": "test-user-123",
        "guest_name": "Иван Тестовый",
        "persons_count": 2,
        "reservation_date": "2024-12-25",
        "reservation_time": "19:00"
    }
    response = requests.post(f"{URL}/table-reservations", json=reservation_data)
    assert response.status_code == 200, "Не удалось забронировать столик"
    reservation = response.json()
    print(f"\tЗабронирован столик номер {reservation['table_number']}")

    # Получение списак заказов
    print("Тест5: Получение заказов")
    response = requests.get(f"{URL}/orders")
    assert response.status_code == 200, "Не удалось получить список заказов"
    orders = response.json()
    print(f"\tЗаказы получены. Всего заказов: {len(orders)}")

if __name__ == "__main__":
    component_tests()