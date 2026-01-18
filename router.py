from fastapi import APIRouter, Depends, status, Query
import crud
from config.database import get_db
from schemas import (
    ItemOrderRequest,
    ItemRequest,
    ItemResponse,
    PaginationParams,
)
from exceptions import NotFoundException

items_router = APIRouter(prefix="/items", tags=["Items"])


def paginated_response(page, page_size, total, **kwargs):
    return {"page": page, "page_size": page_size, "total": total, **kwargs}


@items_router.get(path="/")
def get_items(pagination_params: PaginationParams = Query(None), db=Depends(get_db)):
    items, total = crud.get_items(pagination_params, db)
    # return ItemsResponse(**paginationParams.model_dump(), total = total, items = items)
    return paginated_response(
        pagination_params.page, pagination_params.page_size, total, items=items
    )
    # return {
    #     "page": paginationParams.page,
    #     "page_size": paginationParams.page_size,
    #     "total": total,
    #     "items": items
    #     }


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
def create_order(db=Depends(get_db)):
    return crud.create_order(db)


@router.get(path="/")
def get_orders(pagination_params: PaginationParams = Query(), db=Depends(get_db)):
    orders, total = crud.get_orders(pagination_params, db)
    return paginated_response(
        pagination_params.page, pagination_params.page_size, total, orders=orders
    )


@router.get(path="/{order_id}")
def get_order(order_id: int, db=Depends(get_db)):
    order = crud.get_order(order_id, db)
    if not order:
        raise NotFoundException()
    return order


@router.delete(path="/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db=Depends(get_db)):
    crud.delete_order(order_id, db)


@router.post(
    path="/{order_id}/items",
    responses={status.HTTP_409_CONFLICT: {"description": "Запись уже существует"}},
)
def add_item_to_order(order_id: int, item: ItemOrderRequest, db=Depends(get_db)):
    return crud.add_item_to_order(order_id, item, db)


@router.get(path="/{order_id}/items")
def get_items_from_order(order_id: int, db=Depends(get_db)):
    return crud.get_items_from_order(order_id, db)


@router.delete(
    path="/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_item_from_order(order_id: int, item_id: int, db=Depends(get_db)):
    crud.remove_item_from_order(order_id, item_id, db)


admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.post(path="/items")
def add_item(item: ItemRequest, db=Depends(get_db)) -> ItemResponse:
    return crud.add_item(item, db)


@admin_router.delete(path="/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db=Depends(get_db)):
    crud.delete_item(item_id, db)
