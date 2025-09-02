from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SAEnum

from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    sku = Column(String(60), unique=True, index=True, nullable=False)
    category = Column(String(80), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)

    # relação com movimentações
    movements = relationship(
        "Movement",
        back_populates="product",
        cascade="all, delete-orphan"
    )

# tipo de movimentação
class MovementType(str, Enum):
    IN = "in"
    OUT = "out"


class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False)
    type = Column(SAEnum(MovementType, name="movement_type"), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String(50), nullable=True)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # relação inversa
    product = relationship("Product", back_populates="movements")

