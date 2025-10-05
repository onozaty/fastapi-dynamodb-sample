from uuid import uuid4

from pynamodb.exceptions import DoesNotExist

from app.schemas.item import ItemCreate, ItemResponse
from app.tables.item import ItemTable


class ItemRepository:
    """PynamoDBを使用してアイテムを管理するリポジトリ。"""

    def create_item(self, item: ItemCreate) -> ItemResponse:
        """DynamoDBに新しいアイテムを作成する。"""
        item_id = str(uuid4())

        # PynamoDBモデルを作成
        db_item = ItemTable(
            id=item_id,
            name=item.name,
            # 空文字列をNoneに変換
            description=self._normalize_description(item.description),
            price=item.price,
        )
        db_item.save()

        # Pydanticモデルに変換して返す
        return ItemResponse(
            id=db_item.id,
            name=db_item.name,
            description=db_item.description,
            price=int(db_item.price),  # Decimal -> int
        )

    def get_item(self, item_id: str) -> ItemResponse | None:
        """DynamoDBからIDでアイテムを取得する。"""
        try:
            db_item = ItemTable.get(item_id)
            return ItemResponse(
                id=db_item.id,
                name=db_item.name,
                description=db_item.description,
                price=int(db_item.price),
            )
        except DoesNotExist:
            return None

    def get_all_items(self) -> list[ItemResponse]:
        """DynamoDBから全てのアイテムを取得する。"""
        items: list[ItemResponse] = []
        for db_item in ItemTable.scan():
            items.append(
                ItemResponse(
                    id=db_item.id,
                    name=db_item.name,
                    description=db_item.description,
                    price=int(db_item.price),
                )
            )
        return items

    @staticmethod
    def _normalize_description(description: str | None) -> str | None:
        """DynamoDBストレージ用にdescriptionを正規化する。

        空文字列をNoneに変換してDynamoDBの属性を省略することで、
        ストレージコストを削減し、スパースインデックスを有効にする。

        Args:
            description: 入力からのdescription値。

        Returns:
            descriptionが空または空白のみの場合はNone、それ以外は元の値。
        """
        if description is None:
            return None
        if isinstance(description, str) and not description.strip():
            return None
        return description
