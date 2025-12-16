import pytest
import requests
import json
from datetime import datetime, timedelta


class TestAmenityServiceIntegration:

    def setup_method(self):
        self.base_url = "http://localhost:8003/api"
        self.created_amenities = []
        self.created_orders = []

    def teardown_method(self):
        # Очистка созданных данных (в реальном проекте через API)
        pass

    def test_service_health(self):
        """Тест доступности сервиса"""
        response = requests.get("http://localhost:8003/health", timeout=5)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_amenity(self):
        """Тест создания услуги"""
        amenity_data = {
            "name": "Интеграционный тест - Трансфер",
            "description": "Трансфер из аэропорта для теста",
            "price": 1500.00,
            "category": "transport",
            "duration_minutes": 60
        }

        response = requests.post(
            f"{self.base_url}/amenities",
            json=amenity_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        amenity = response.json()
        self.created_amenities.append(amenity["id"])

        assert amenity["name"] == amenity_data["name"]
        assert amenity["price"] == amenity_data["price"]

    def test_get_amenities(self):
        """Тест получения списка услуг"""
        response = requests.get(f"{self.base_url}/amenities")
        assert response.status_code == 200

        amenities = response.json()
        assert isinstance(amenities, list)

    def test_create_and_get_amenity_order(self):
        """Тест создания и получения заказа услуги"""
        # Сначала создаем услугу
        amenity_response = requests.post(f"{self.base_url}/amenities", json={
            "name": "Тестовая услуга для заказа",
            "price": 2000.00,
            "category": "spa",
            "duration_minutes": 60
        })
        assert amenity_response.status_code == 200
        amenity = amenity_response.json()

        # Создаем заказ
        scheduled_time = (datetime.now() + timedelta(days=1)).isoformat()
        order_data = {
            "guest_id": "integration-test-guest",
            "guest_name": "Тестовый Гость",
            "amenity_id": amenity["id"],
            "scheduled_for": scheduled_time,
            "guest_notes": "Тестовый заказ"
        }

        order_response = requests.post(
            f"{self.base_url}/amenity-orders",
            json=order_data
        )
        assert order_response.status_code == 200
        order = order_response.json()
        self.created_orders.append(order["order_id"])

        # Получаем заказ
        detail_response = requests.get(f"{self.base_url}/amenity-orders/{order['order_id']}")
        assert detail_response.status_code == 200
        order_detail = detail_response.json()

        assert order_detail["id"] == order["order_id"]
        assert order_detail["guest_id"] == order_data["guest_id"]

    def test_amenity_order_workflow(self):
        """Полный workflow заказа услуги"""
        # Создаем услугу
        amenity_response = requests.post(f"{self.base_url}/amenities", json={
            "name": "Workflow тест услуга",
            "price": 3000.00,
            "category": "tour",
            "duration_minutes": 120
        })
        amenity = amenity_response.json()

        # Создаем заказ
        scheduled_time = (datetime.now() + timedelta(days=1)).isoformat()
        order_response = requests.post(f"{self.base_url}/amenity-orders", json={
            "guest_id": "workflow-test-guest",
            "guest_name": "Workflow Тест",
            "amenity_id": amenity["id"],
            "scheduled_for": scheduled_time
        })
        order = order_response.json()
        order_id = order["order_id"]

        # Назначаем сотрудника
        assign_response = requests.patch(
            f"{self.base_url}/amenity-orders/{order_id}/assign",
            json={
                "staff_id": "test-staff-001",
                "staff_name": "Тестовый Сотрудник"
            }
        )
        assert assign_response.status_code == 200
        assigned_order = assign_response.json()
        assert assigned_order["status"] == "assigned"

        # Завершаем заказ
        complete_response = requests.patch(
            f"{self.base_url}/amenity-orders/{order_id}/complete",
            json={"notes": "Услуга предоставлена"}
        )
        assert complete_response.status_code == 200
        completed_order = complete_response.json()
        assert completed_order["status"] == "completed"


# Функции для запуска напрямую
def run_integration_tests():
    """Запуск интеграционных тестов напрямую"""
    print("🚀 Запуск интеграционных тестов для Amenity Service...")

    tester = TestAmenityServiceIntegration()

    test_methods = [
        "test_service_health",
        "test_create_amenity",
        "test_get_amenities",
        "test_create_and_get_amenity_order",
        "test_amenity_order_workflow"
    ]

    for method_name in test_methods:
        tester.setup_method()
        try:
            method = getattr(tester, method_name)
            method()
            print(f"✅ {method_name} - PASSED")
        except Exception as e:
            print(f"❌ {method_name} - FAILED: {e}")
        finally:
            tester.teardown_method()


if __name__ == "__main__":
    run_integration_tests()