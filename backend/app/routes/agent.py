from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import AdviceRequest, AdviceResponse, CompareAdviceResponse
from app.services.agent import decision_agent

router = APIRouter(prefix="/api/agent", tags=["AI Advisor"])

@router.post("/advice", response_model=AdviceResponse)
def get_advice(request: AdviceRequest, db: Session = Depends(get_db)):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return decision_agent.get_advice(db, request)

@router.post("/compare", response_model=CompareAdviceResponse)
def compare_advice(request: AdviceRequest, db: Session = Depends(get_db)):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return decision_agent.compare_advice(db, request.question, domain=request.domain or "Both")
