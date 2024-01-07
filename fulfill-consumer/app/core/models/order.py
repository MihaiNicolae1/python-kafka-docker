from sqlalchemy import Column, String, Integer
from app.dependencies.db import Base


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255))
    address = Column(String(255))
    items = Column(String(255))
