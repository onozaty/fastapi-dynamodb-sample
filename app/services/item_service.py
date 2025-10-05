from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemResponse


class ItemService:
    """アイテムのビジネスロジックを提供するサービス。"""

    def __init__(self) -> None:
        """ItemServiceを初期化する。"""
        self.repository = ItemRepository()

    def create_item(self, item: ItemCreate) -> ItemResponse:
        """新しいアイテムを作成する。

        Args:
            item: 作成するアイテムの情報。

        Returns:
            作成されたアイテムのレスポンス。
        """
        return self.repository.create_item(item)

    def get_item(self, item_id: str) -> ItemResponse | None:
        """IDでアイテムを取得する。

        Args:
            item_id: 取得するアイテムのID。

        Returns:
            取得したアイテムのレスポンス。見つからない場合はNone。
        """
        return self.repository.get_item(item_id)

    def get_items(self) -> list[ItemResponse]:
        """全てのアイテムを取得する。

        Returns:
            全てのアイテムのリスト。
        """
        return self.repository.get_all_items()
