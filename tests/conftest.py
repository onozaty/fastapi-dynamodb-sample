from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.db.dynamodb import ensure_all_tables_exist
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client with a fresh DynamoDB table for each test."""

    with mock_aws():
        ensure_all_tables_exist()
        yield TestClient(app)
