from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(title="アイテムの名前", max_length=100, examples=["Apple"])
    description: str | None = Field(
        default=None,
        title="アイテムの説明",
        max_length=300,
        examples=["A juicy red apple"],
    )
    price: int = Field(title="アイテムの価格", examples=[100])


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: str = Field(
        title="アイテムのID",
        examples=["01937c6e-77b2-7f9e-ae59-8e579f5e6c7e"],
    )
