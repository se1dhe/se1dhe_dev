from fastapi.testclient import TestClient
from ..main import app
import pytest
from datetime import datetime

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_bot():
    response = client.post(
        "/api/bots/",
        json={
            "name": "Test Bot",
            "description": "Test Description",
            "price": 10.0,
            "category_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Bot"
    assert "id" in data

def test_create_review():
    response = client.post(
        "/api/reviews/",
        json={
            "user_id": 1,
            "bot_id": 1,
            "rating": 5,
            "comment": "Great bot!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert "id" in data

def test_create_notification():
    response = client.post(
        "/api/notifications/",
        json={
            "user_id": 1,
            "type": "system",
            "channel": "email",
            "title": "Test Notification",
            "message": "Test Message"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Notification"
    assert "id" in data

def test_track_analytics_event():
    response = client.post(
        "/api/analytics/events/",
        json={
            "user_id": 1,
            "event_type": "page_view",
            "event_data": {"page": "home"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "page_view"
    assert "id" in data

def test_create_ab_test():
    response = client.post(
        "/api/ab-tests/",
        json={
            "name": "Test AB Test",
            "type": "ui_changes",
            "variants": {
                "A": {"color": "red"},
                "B": {"color": "blue"}
            },
            "metrics": ["conversion_rate"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test AB Test"
    assert "id" in data

def test_start_ab_test():
    # Сначала создаем тест
    create_response = client.post(
        "/api/ab-tests/",
        json={
            "name": "Test AB Test",
            "type": "ui_changes",
            "variants": {"A": {}, "B": {}},
            "metrics": ["conversion_rate"]
        }
    )
    test_id = create_response.json()["id"]

    # Затем запускаем его
    response = client.post(f"/api/ab-tests/{test_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"

def test_record_ab_test_result():
    # Создаем тест
    create_response = client.post(
        "/api/ab-tests/",
        json={
            "name": "Test AB Test",
            "type": "ui_changes",
            "variants": {"A": {}, "B": {}},
            "metrics": ["conversion_rate"]
        }
    )
    test_id = create_response.json()["id"]

    # Запускаем тест
    client.post(f"/api/ab-tests/{test_id}/start")

    # Записываем результат
    response = client.post(
        "/api/ab-tests/results/",
        json={
            "test_id": test_id,
            "variant": "A",
            "metrics_data": {"conversion_rate": 0.5}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["variant"] == "A"
    assert "id" in data 