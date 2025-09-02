from typing import List, Optional, cast

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/movements", tags=["Movements"])


@router.post("", response_model=schemas.MovementOut, status_code=201)
def create_movement(payload: schemas.MovementCreate, db: Session = Depends(get_db)):
    """
    Cria uma movimentação (entrada/saída) e atualiza o estoque do produto.
    Usa SELECT ... FOR UPDATE pra evitar corrida.
    """
    product = (
        db.query(models.Product)
        .filter(models.Product.id == payload.product_id)
        .with_for_update()
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ajuda o Pylance: em runtime já é int
    current_qty = cast(int, product.quantity)

    if payload.type == "out":
        if current_qty - payload.quantity < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.quantity = current_qty - payload.quantity  # type: ignore[assignment]
    else:  # "in"
        product.quantity = current_qty + payload.quantity  # type: ignore[assignment]

    movement = models.Movement(
        product_id=payload.product_id,
        type=payload.type,  # Literal["in","out"] casa com o Enum do model
        quantity=payload.quantity,
        reason=payload.reason,
        notes=payload.notes,
    )

    db.add(movement)
    db.add(product)
    db.commit()
    db.refresh(movement)
    return movement


@router.get("", response_model=List[schemas.MovementOut])
def list_movements(
    db: Session = Depends(get_db),
    product_id: Optional[int] = Query(None),
    type: Optional[schemas.MovementType] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    Lista movimentos com filtros opcionais e paginação simples.
    """
    q = db.query(models.Movement)
    if product_id is not None:
        q = q.filter(models.Movement.product_id == product_id)
    if type is not None:
        q = q.filter(models.Movement.type == type)  # type: ignore[arg-type]
    q = q.order_by(models.Movement.created_at.desc())
    return q.offset(offset).limit(limit).all()


@router.get("/products/{product_id}", response_model=List[schemas.MovementOut])
def list_product_movements(product_id: int, db: Session = Depends(get_db)):
    """
    Histórico de movimentos de um produto específico.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return (
        db.query(models.Movement)
        .filter(models.Movement.product_id == product_id)
        .order_by(models.Movement.created_at.desc())
        .all()
    )
