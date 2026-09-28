from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import EngineeringDecision
from app.schemas.schemas import EngineeringDecisionCreate, EngineeringDecisionRead
from app.services.decision_memory import memory_manager

router = APIRouter(prefix="/api/engineering-decisions", tags=["Engineering Decisions"])

@router.post("", response_model=EngineeringDecisionRead)
def create_engineering_decision(ed_in: EngineeringDecisionCreate, db: Session = Depends(get_db)):
    ed_count = db.query(EngineeringDecision).count()
    ed_id = f"ED-{215 + ed_count}"

    rejected_dicts = [alt.dict() if hasattr(alt, "dict") else alt for alt in ed_in.rejected_alternatives]

    ed = EngineeringDecision(
        id=ed_id,
        title=ed_in.title,
        problem=ed_in.problem,
        context=ed_in.context,
        decision=ed_in.decision,
        alternatives_considered=ed_in.alternatives_considered,
        rejected_alternatives=rejected_dicts,
        constraints=ed_in.constraints,
        trade_offs=ed_in.trade_offs,
        expected_consequences=ed_in.expected_consequences,
        actual_consequences=ed_in.actual_consequences,
        technology=ed_in.technology,
        architecture_area=ed_in.architecture_area,
        date=ed_in.date,
        status=ed_in.status or "Accepted",
        related_product_decision_id=ed_in.related_product_decision_id,
        related_feedback_id=ed_in.related_feedback_id
    )
    db.add(ed)
    db.commit()
    db.refresh(ed)

    # Retain ADR experience in Hindsight & PostgreSQL memory
    memory_manager.retain_engineering_decision_experience(db, ed)

    return ed

@router.get("", response_model=List[EngineeringDecisionRead])
def get_engineering_decisions(
    technology: Optional[str] = None,
    architecture_area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EngineeringDecision)
    if technology:
        query = query.filter(EngineeringDecision.technology == technology)
    if architecture_area:
        query = query.filter(EngineeringDecision.architecture_area == architecture_area)
    return query.order_by(EngineeringDecision.date.desc()).all()

@router.get("/{decision_id}", response_model=EngineeringDecisionRead)
def get_engineering_decision_detail(decision_id: str, db: Session = Depends(get_db)):
    ed = db.query(EngineeringDecision).filter(EngineeringDecision.id == decision_id).first()
    if not ed:
        raise HTTPException(status_code=404, detail="Engineering decision not found")
    return ed
