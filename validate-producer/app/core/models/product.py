from sqlalchemy import Column, Integer, String
from app.dependencies.db import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    stock = Column(Integer)
    title = Column(String(255))
    name = Column(String(255))
    description = Column(String(512))
