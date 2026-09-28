from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import ArchitectureDecision
from app.schemas.schemas import ArchitectureDecisionCreate, ArchitectureDecisionRead

router = APIRouter(prefix="/api/architecture-decisions", tags=["Architecture Decisions"])

@router.post("", response_model=ArchitectureDecisionRead)
def create_architecture_decision(ad_in: ArchitectureDecisionCreate, db: Session = Depends(get_db)):
    ad_count = db.query(ArchitectureDecision).count()
    ad_id = f"AD-{308 + ad_count}"

    ad = ArchitectureDecision(
        id=ad_id,
        title=ad_in.title,
        status=ad_in.status or "Accepted",
        date=ad_in.date,
        technology=ad_in.technology,
        problem=ad_in.problem,
        context=ad_in.context,
        constraints=ad_in.constraints,
        options=ad_in.options,
        decision=ad_in.decision,
        trade_offs=ad_in.trade_offs,
        consequences=ad_in.consequences,
        related_decisions=ad_in.related_decisions
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad

@router.get("", response_model=List[ArchitectureDecisionRead])
def get_architecture_decisions(
    technology: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ArchitectureDecision)
    if technology:
        query = query.filter(ArchitectureDecision.technology == technology)
    return query.order_by(ArchitectureDecision.date.desc()).all()

@router.get("/{decision_id}", response_model=ArchitectureDecisionRead)
def get_architecture_decision_detail(decision_id: str, db: Session = Depends(get_db)):
    ad = db.query(ArchitectureDecision).filter(ArchitectureDecision.id == decision_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Architecture decision not found")
    return ad
