from pydantic import BaseModel, condecimal
from typing import Optional

class ProductBase(BaseModel):
    name: str
    sku: str
    category: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: int = 0
    min_stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    quantity: Optional[int] = None
    min_stock: Optional[int] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True  # pydantic v2
