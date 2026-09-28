from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Feedback, ProductDecision, EngineeringDecision, Experiment, Outcome
from app.schemas.schemas import TimelineEventRead

router = APIRouter(prefix="/api/timeline", tags=["Timeline"])

@router.get("", response_model=List[TimelineEventRead])
def get_timeline(db: Session = Depends(get_db)):
    events = []

    # Feedbacks
    feedbacks = db.query(Feedback).all()
    for f in feedbacks:
        events.append(TimelineEventRead(
            id=f"TL-FB-{f.id}",
            date=f.date,
            type="Problem",
            title=f"Customer Feedback [{f.customer_name}]",
            description=f.content,
            product_area=f.product_area,
            status=f.status,
            related_id=f.id
        ))

    # Product Decisions
    pds = db.query(ProductDecision).all()
    for p in pds:
        events.append(TimelineEventRead(
            id=f"TL-PD-{p.id}",
            date=p.date,
            type="Product Decision",
            title=f"Product Decision: {p.title}",
            description=f"Chosen Approach: {p.chosen_approach}. Reason: {p.reason}",
            product_area=p.product_area,
            status=p.status,
            related_id=p.id
        ))

    # Engineering Decisions
    eds = db.query(EngineeringDecision).all()
    for e in eds:
        events.append(TimelineEventRead(
            id=f"TL-ED-{e.id}",
            date=e.date,
            type="Engineering Decision",
            title=f"ADR: {e.title}",
            description=f"Decision: {e.decision}. Technology: {e.technology}. Trade-offs: {e.trade_offs or 'N/A'}",
            product_area=e.architecture_area,
            technology=e.technology,
            status=e.status,
            related_id=e.id
        ))

    # Experiments
    exps = db.query(Experiment).all()
    for ex in exps:
        events.append(TimelineEventRead(
            id=f"TL-EXP-{ex.id}",
            date=ex.start_date,
            type="Experiment",
            title=f"Experiment: {ex.name}",
            description=f"Hypothesis: {ex.hypothesis}. Result: {ex.result or 'In progress'}",
            product_area=ex.product_area,
            status=ex.status,
            related_id=ex.id
        ))

    # Outcomes
    outcomes = db.query(Outcome).all()
    for o in outcomes:
        events.append(TimelineEventRead(
            id=f"TL-OUT-{o.id}",
            date=o.date,
            type="Outcome",
            title=f"Observed Outcome: {o.title}",
            description=f"{o.description} Impact: {o.metrics_impact or 'N/A'}",
            product_area=o.category,
            status="Measured",
            related_id=o.id
        ))

    # Sort events chronologically ascending
    events.sort(key=lambda x: x.date)
    return events
