from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    category_id: int


class ProductCreate(ProductBase):
    tag_ids: Optional[List[int]] = []


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    image: str | None = None
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
