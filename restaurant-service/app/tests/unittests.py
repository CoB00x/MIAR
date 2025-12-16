import requests
import json


def test_restaurant_service():
    """Простой тест ресторанного сервиса через HTTP"""
    base_url = "http://localhost:8002/api"

    print("Тестирование Restaurant Service...")

    # 1. Тест получения меню
    print("1. Тест получения меню...")
    response = requests.get(f"{base_url}/menu")
    if response.status_code == 200:
        print("   Меню получено успешно")
    else:
        print(f"   Ошибка: {response.status_code}")
        return

    # 2. Тест создания блюда
    print("2. Тест создания блюда...")
    menu_item = {
        "name": "Тестовое блюдо",
        "description": "Создано для тестирования",
        "price": 999.99,
        "category": "test",
        "preparation_time": 10
    }

    response = requests.post(
        f"{base_url}/menu/items",
        json=menu_item,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        created_item = response.json()
        print("   Блюдо создано успешно")
        item_id = created_item["id"]
    else:
        print(f"   Ошибка создания блюда: {response.status_code}")
        return

    # 3. Тест создания заказа
    print("3. Тест создания заказа...")
    order_data = {
        "guest_id": "test-guest-001",
        "order_type": "in_restaurant",
        "items": [{"menu_item_id": item_id, "quantity": 1}]
    }

    response = requests.post(
        f"{base_url}/orders",
        json=order_data,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        order = response.json()
        print("   Заказ создан успешно")
        print(f"   Статус заказа: {order['status']}")
        print(f"   Сумма: {order['total_amount']}")
    else:
        print(f"   Ошибка создания заказа: {response.status_code}")
        return

    print("\nВсе тесты пройдены успешно!")


if __name__ == "__main__":
    test_restaurant_service()