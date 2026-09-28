from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import ProductDecision
from app.schemas.schemas import ProductDecisionCreate, ProductDecisionRead
from app.services.decision_memory import memory_manager

router = APIRouter(prefix="/api/product-decisions", tags=["Product Decisions"])

@router.post("", response_model=ProductDecisionRead)
def create_product_decision(pd_in: ProductDecisionCreate, db: Session = Depends(get_db)):
    pd_count = db.query(ProductDecision).count()
    pd_id = f"PD-{110 + pd_count}"

    pd = ProductDecision(
        id=pd_id,
        title=pd_in.title,
        problem=pd_in.problem,
        context=pd_in.context,
        options_considered=pd_in.options_considered,
        chosen_approach=pd_in.chosen_approach,
        reason=pd_in.reason,
        expected_outcome=pd_in.expected_outcome,
        actual_outcome=pd_in.actual_outcome,
        date=pd_in.date,
        status=pd_in.status or "Accepted",
        product_area=pd_in.product_area,
        related_feedback_id=pd_in.related_feedback_id
    )
    db.add(pd)
    db.commit()
    db.refresh(pd)

    # Retain in Hindsight and PostgreSQL memory
    memory_manager.retain_product_decision_experience(db, pd)

    return pd

@router.get("", response_model=List[ProductDecisionRead])
def get_product_decisions(
    product_area: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductDecision)
    if product_area:
        query = query.filter(ProductDecision.product_area == product_area)
    if status:
        query = query.filter(ProductDecision.status == status)
    return query.order_by(ProductDecision.date.desc()).all()

@router.get("/{decision_id}", response_model=ProductDecisionRead)
def get_product_decision_detail(decision_id: str, db: Session = Depends(get_db)):
    pd = db.query(ProductDecision).filter(ProductDecision.id == decision_id).first()
    if not pd:
        raise HTTPException(status_code=404, detail="Product decision not found")
    return pd
