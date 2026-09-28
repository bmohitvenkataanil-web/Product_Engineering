from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Feedback
from app.schemas.schemas import FeedbackCreate, FeedbackRead, FeedbackAnalyzeResponse
from app.services.decision_memory import memory_manager
from app.services.agent import decision_agent

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackRead)
def create_feedback(feedback_in: FeedbackCreate, db: Session = Depends(get_db)):
    fb_count = db.query(Feedback).count()
    fb_id = f"FB-{1050 + fb_count}"
    
    fb = Feedback(
        id=fb_id,
        customer_id=feedback_in.customer_id,
        customer_name=feedback_in.customer_name,
        content=feedback_in.content,
        product_area=feedback_in.product_area,
        sentiment=feedback_in.sentiment or "Neutral",
        priority=feedback_in.priority or "Medium",
        date=feedback_in.date,
        status=feedback_in.status or "Open"
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)

    # Retain feedback experience in memory
    memory_manager.retain_feedback_experience(db, fb)

    return fb

@router.get("", response_model=List[FeedbackRead])
def get_feedbacks(
    product_area: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Feedback)
    if product_area:
        query = query.filter(Feedback.product_area == product_area)
    if status:
        query = query.filter(Feedback.status == status)
    return query.order_by(Feedback.date.desc()).all()

@router.get("/{feedback_id}", response_model=FeedbackRead)
def get_feedback_detail(feedback_id: str, db: Session = Depends(get_db)):
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return fb

@router.post("/{feedback_id}/analyze", response_model=FeedbackAnalyzeResponse)
def analyze_feedback(
    feedback_id: str,
    memory_mode: str = Query("ON", description="ON or OFF"),
    db: Session = Depends(get_db)
):
    try:
        return decision_agent.analyze_feedback(db, feedback_id, memory_mode=memory_mode)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
