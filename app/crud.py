from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models import Order, OrderItem, Item
from fastapi import HTTPException, status
from app.schemas import (
    OrderResponse,
    ItemRequest,
    ItemResponse,
    ItemOrderRequest,
    PaginationParams,
)
from app.exceptions import AlreadyExistsException, NotFoundException, ItemNotFoundException


def create_order(db: Session) -> OrderResponse:
    db_order = Order()
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def __query_with_pagination(entity, pagination_params: PaginationParams, db: Session):
    page = pagination_params.page
    page_size = pagination_params.page_size
    db_items = db.query(entity).offset((page - 1) * page_size).limit(page_size).all()
    total = db.query(entity).count()
    return db_items, total
    # return ItemsResponse(page=page, pageSize=page_size, total=total, items=db_items)
    # return {
    #     "page": page,
    #     "pageSize": page_size,
    #     "total": total,
    #     "items": db_items
    #     }


def get_orders(pagination_params: PaginationParams, db: Session):
    return __query_with_pagination(Order, pagination_params, db)


def get_order(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()


def get_items(
    pagination_params: PaginationParams, db: Session
) -> tuple[list[ItemResponse], int]:
    return __query_with_pagination(Item, pagination_params, db)


def add_item_to_order(order_id: int, item: ItemOrderRequest, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NotFoundException()

    db_item = db.query(Item).filter(Item.id == item.item_id).first()
    if not db_item:
        raise ItemNotFoundException(item.item_id)
    order_item_result = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id, OrderItem.item_id == item.item_id)
        .first()
    )
    if order_item_result:
        raise AlreadyExistsException()
    db_order_item = OrderItem(
        order_id=order_id, item_id=item.item_id, amount=item.amount
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    # item = db.query(Item).filter(Item.id == db_order_item.item_id).first() # кажется, что как-то проще можно сделать, без дополнительного запроса .query()
    print("db_item: ", db_item)
    db.refresh(db_item)
    return db_item


def delete_order(order_id: int, db: Session):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise NotFoundException()
    db.delete(db_order)
    db.commit()


def remove_item_from_order(order_id: int, item_id: int, db: Session):
    db_order_item = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id, OrderItem.item_id == item_id)
        .first()
    )
    if not db_order_item:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            raise NotFoundException()
        raise NotFoundException(f"Продукта с id = {item_id} нет в заказе")
    db.delete(db_order_item)
    db.commit()


def add_item(item: ItemRequest, db: Session) -> ItemResponse:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(item_id: int, db: Session):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise NotFoundException(f"Продукта с id = {item_id} нет")
    try:
        db.delete(db_item)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Продукт не может быть удален, есть заказы с продуктом с id = {item_id}",
        )


def get_items_from_order(order_id: int, db: Session):
    order_and_items = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not order_and_items:
        order_exists = db.query(Order).filter(Order.id == order_id).first()
        if not order_exists:
            raise NotFoundException()
    return order_and_items
