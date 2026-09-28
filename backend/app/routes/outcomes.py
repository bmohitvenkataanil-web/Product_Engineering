from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Outcome
from app.schemas.schemas import OutcomeCreate, OutcomeRead
from app.services.decision_memory import memory_manager

router = APIRouter(prefix="/api/outcomes", tags=["Outcomes"])

@router.post("", response_model=OutcomeRead)
def create_outcome(outcome_in: OutcomeCreate, db: Session = Depends(get_db)):
    out_count = db.query(Outcome).count()
    out_id = f"OUT-{215 + out_count}"

    out = Outcome(
        id=out_id,
        title=outcome_in.title,
        description=outcome_in.description,
        category=outcome_in.category or "Product Performance",
        metrics_impact=outcome_in.metrics_impact,
        date=outcome_in.date,
        related_decision_type=outcome_in.related_decision_type,
        related_decision_id=outcome_in.related_decision_id
    )
    db.add(out)
    db.commit()
    db.refresh(out)

    # Retain outcome experience in Hindsight & PostgreSQL
    memory_manager.retain_outcome_experience(db, out)

    return out

@router.get("", response_model=List[OutcomeRead])
def get_outcomes(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Outcome)
    if category:
        query = query.filter(Outcome.category == category)
    return query.order_by(Outcome.date.desc()).all()

@router.get("/{outcome_id}", response_model=OutcomeRead)
def get_outcome_detail(outcome_id: str, db: Session = Depends(get_db)):
    out = db.query(Outcome).filter(Outcome.id == outcome_id).first()
    if not out:
        raise HTTPException(status_code=404, detail="Outcome not found")
    return out
