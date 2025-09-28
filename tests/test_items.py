from fastapi.testclient import TestClient


def test_create_item(client: TestClient) -> None:
    response = client.post(
        "/items/",
        json={"name": "Apple", "description": "Juicy", "price": 120},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["name"] == "Apple"
    assert payload["description"] == "Juicy"
    assert payload["price"] == 120


def test_get_items_returns_all_created_items(client: TestClient) -> None:
    client.post(
        "/items/",
        json={"name": "Apple", "description": "Juicy", "price": 120},
    )
    client.post(
        "/items/",
        json={"name": "Banana", "description": "Sweet", "price": 80},
    )

    response = client.get("/items/")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["name"] == "Apple"
    assert payload[1]["name"] == "Banana"


def test_get_item_returns_single_item(client: TestClient) -> None:
    client.post(
        "/items/",
        json={"name": "Apple", "description": "Juicy", "price": 120},
    )

    response = client.get("/items/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["name"] == "Apple"


def test_get_item_returns_404_when_missing(client: TestClient) -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
