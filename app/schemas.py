from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class OrderRequest(BaseModel):
    pass


class OrderResponse(BaseModel):
    status: str = Field(...)
    created_at: datetime
    deleted_at: Optional[datetime]
    updated_at: Optional[datetime]


class ItemOrderRequest(BaseModel):
    item_id: int = Field(...)
    amount: Optional[int] = Field(default=1, gt=0)


class ItemOrderResponse(BaseModel):
    id: int
    price: float
    amount: int


class ItemRequest(BaseModel):
    price: float = Field(..., ge=0)
    amount: int = Field(..., gt=0)
    name: str = Field(...)


class ItemResponse(BaseModel):
    id: int
    price: float
    amount: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=0)


class ItemsResponse(BaseModel):
    page: int
    pageSize: int
    total: int
    items: list[ItemResponse]
