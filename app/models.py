from sqlalchemy import Column, Integer, String, Numeric
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    category = Column(String(80), nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)
