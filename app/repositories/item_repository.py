from uuid import uuid4

from pynamodb.exceptions import DoesNotExist

from app.schemas.item import ItemCreate, ItemResponse
from app.tables.item import ItemTable


class ItemRepository:
    """Repository for managing items using PynamoDB."""

    def create_item(self, item: ItemCreate) -> ItemResponse:
        """Create a new item in DynamoDB."""
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
        """Get an item by ID from DynamoDB."""
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
        """Get all items from DynamoDB."""
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
        """Normalize description for DynamoDB storage.

        Convert empty strings to None to omit the attribute in DynamoDB,
        which saves storage costs and enables sparse indexes.

        Args:
            description: The description value from the input.

        Returns:
            None if the description is empty or whitespace-only, otherwise the
            original value.
        """
        if description is None:
            return None
        if isinstance(description, str) and not description.strip():
            return None
        return description
