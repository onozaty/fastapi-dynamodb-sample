from app.schemas.item import ItemCreate, ItemResponse

fake_items_db: list[ItemResponse] = []
current_id = 0


class ItemService:
    def create_item(self, item: ItemCreate) -> ItemResponse:
        global current_id
        current_id += 1
        created_item = ItemResponse(id=current_id, **item.model_dump())
        fake_items_db.append(created_item)
        return created_item

    def get_item(self, item_id: int) -> ItemResponse | None:
        for item in fake_items_db:
            if item.id == item_id:
                return item
        return None

    def get_items(self) -> list[ItemResponse]:
        return fake_items_db.copy()
