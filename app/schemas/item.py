from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(title="The name of the item", max_length=100, examples=["Apple"])
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300,
        examples=["A juicy red apple"],
    )
    price: int = Field(title="The price of the item", examples=[100])


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: str = Field(
        title="The ID of the item",
        examples=["01937c6e-77b2-7f9e-ae59-8e579f5e6c7e"],
    )
