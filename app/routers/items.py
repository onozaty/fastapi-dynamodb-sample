from fastapi import APIRouter, Depends, HTTPException

from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate, svc: ItemService = Depends()) -> ItemResponse:
    return svc.create_item(item)


@router.get("/", response_model=list[ItemResponse])
async def get_items(svc: ItemService = Depends()) -> list[ItemResponse]:
    return svc.get_items()


@router.get(
    "/{item_id}",
    response_model=ItemResponse | None,
    responses={
        404: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        },
    },
)
async def get_item(item_id: int, svc: ItemService = Depends()) -> ItemResponse | None:
    item = svc.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
