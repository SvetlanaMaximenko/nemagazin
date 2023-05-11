from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from .db import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    cost = Column(Integer)
    count = Column(Integer)
    order = relationship("Orders", back_populates="product")

    def __str__(self):
        return f"Product: <{self.name}>"


class Ticket(BaseModel):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(length=26))
    available = Column(Boolean, default=True)
    user = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_id = relationship("User", back_populates="ticket")

    @classmethod
    def is_valid(cls, ticket_uuid: str) -> bool:
        ticket: Ticket = cls.get(uuid=ticket_uuid)
        if ticket is None:
            return False
        return ticket.available and not ticket.user


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    points = Column(Integer)
    ticket = relationship("Ticket", back_populates="user_id")
    order = relationship("Orders", back_populates="user")

    @staticmethod
    def is_exist(username: str) -> bool:
        return User.get(username=username) is not None


class Orders(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="order")
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="order")
    count = Column(Integer)
    order_datetime = Column(DateTime)
