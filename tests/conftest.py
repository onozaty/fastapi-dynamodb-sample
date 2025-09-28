import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import item_service


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_fake_db() -> None:
    item_service.fake_items_db.clear()
    item_service.current_id = 0
