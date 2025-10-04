from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemResponse


class ItemService:
    def __init__(self) -> None:
        self.repository = ItemRepository()

    def create_item(self, item: ItemCreate) -> ItemResponse:
        return self.repository.create_item(item)

    def get_item(self, item_id: str) -> ItemResponse | None:
        return self.repository.get_item(item_id)

    def get_items(self) -> list[ItemResponse]:
        return self.repository.get_all_items()
