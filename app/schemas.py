from datetime import datetime
from typing import Optional, Literal, Annotated
from decimal import Decimal

from pydantic import BaseModel, condecimal, conint

# ---- Aliases pra Pydantic v2 (ajuda o Pylance) ----
Price = Annotated[Decimal, condecimal(max_digits=10, decimal_places=2)]
PositiveInt = Annotated[int, conint(gt=0)]

# =====================
# PRODUCTS (já existiam)
# =====================

class ProductBase(BaseModel):
    name: str
    sku: str
    category: Optional[str] = None
    price: Price
    quantity: int = 0
    min_stock: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Price] = None
    quantity: Optional[int] = None
    min_stock: Optional[int] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        # pydantic v2 (antigo: orm_mode=True)
        from_attributes = True


# =====================
# MOVEMENTS (novos)
# =====================

MovementType = Literal["in", "out"]


class MovementBase(BaseModel):
    product_id: int
    type: MovementType
    quantity: PositiveInt
    reason: Optional[str] = None
    notes: Optional[str] = None


class MovementCreate(MovementBase):
    pass


class MovementOut(BaseModel):
    id: int
    product_id: int
    type: MovementType
    quantity: int
    reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
