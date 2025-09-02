from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    # SKU único
    exists = db.query(models.Product).filter(models.Product.sku == payload.sku).first()
    if exists:
        raise HTTPException(status_code=400, detail="SKU já cadastrado")
    prod = models.Product(**payload.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

@router.get("", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id.desc()).all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, payload: schemas.ProductUpdate, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(prod, k, v)
    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(prod)
    db.commit()
    return None
