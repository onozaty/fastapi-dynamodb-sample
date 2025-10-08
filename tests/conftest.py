from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.main import app
from app.tables.item import ItemTable


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """各テストごとに新しいDynamoDBテーブルを使用してテストクライアントを作成する。"""

    with mock_aws():
        ensure_all_tables_exist()
        yield TestClient(app)


def ensure_all_tables_exist() -> None:
    """全てのDynamoDBテーブルが存在することを確認し、存在しない場合は作成する。"""

    if not ItemTable.exists():
        ItemTable.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True,
        )
