from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey
from app.config.database import BaseModel, TimestampMixin, Base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class Item(BaseModel, TimestampMixin):
    __tablename__ = "items"
    name = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)

    orders = relationship(
        "Order", secondary="order_items", back_populates="items", passive_deletes=True
    )


class User(BaseModel, TimestampMixin):
    __tablename__ = "users"
    username = Column(String(100))
    email = Column(String(100))
    phone = Column(String(100))
    name = Column(String(100))
    surename = Column(String(100))
    patronymic = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="user")


class OrderStatus(str, PyEnum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    FINISHED = "FINISHED"


class Order(BaseModel, TimestampMixin):
    __tablename__ = "orders"
    user_id = Column(Integer, ForeignKey("users.id"), default=1)
    status: Column[OrderStatus] = Column(
        Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False
    )

    user = relationship("User", back_populates="orders")
    items = relationship("Item", secondary="order_items", back_populates="orders")


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True
    )
    item_id = Column(
        Integer, ForeignKey("items.id", ondelete="RESTRICT"), primary_key=True
    )
    amount = Column(Integer)
