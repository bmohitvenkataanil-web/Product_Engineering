from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database import get_db
from app.models.models import MemoryEvent
from app.schemas.schemas import (
    RetainMemoryRequest, RecallMemoryRequest, ReflectMemoryRequest,
    MemoryEventRead, HindsightStatusRead
)
from app.services.hindsight import hindsight_service
from app.services.decision_memory import memory_manager

router = APIRouter(prefix="/api/memory", tags=["Memory"])

@router.post("/retain", response_model=MemoryEventRead)
def retain_memory(req: RetainMemoryRequest, db: Session = Depends(get_db)):
    mem_count = db.query(MemoryEvent).count()
    mem_id = f"MEM-{800 + mem_count}"

    # Retain in Hindsight
    hindsight_res = hindsight_service.retain(
        content=f"{req.summary}\n{req.content}",
        metadata={"memory_type": req.memory_type, "product_area": req.product_area, "technology": req.technology}
    )

    mem_event = MemoryEvent(
        id=mem_id,
        memory_type=req.memory_type,
        summary=req.summary,
        content=req.content,
        product_area=req.product_area,
        technology=req.technology,
        hindsight_memory_id=hindsight_res.get("hindsight_id"),
        date=req.date,
        related_decision_id=req.related_decision_id,
        related_outcome_id=req.related_outcome_id
    )
    db.add(mem_event)
    db.commit()
    db.refresh(mem_event)

    return mem_event

@router.post("/recall")
def recall_memory(req: RecallMemoryRequest):
    return hindsight_service.recall(query=req.query, top_k=req.top_k or 5)

@router.post("/reflect")
def reflect_memory(req: ReflectMemoryRequest):
    reflection = hindsight_service.reflect(query=req.query)
    return {"reflection": reflection or "No reflection synthesized."}

@router.get("/events", response_model=List[MemoryEventRead])
def get_memory_events(
    memory_type: Optional[str] = None,
    product_area: Optional[str] = None,
    technology: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MemoryEvent)
    if memory_type:
        query = query.filter(MemoryEvent.memory_type == memory_type)
    if product_area:
        query = query.filter(MemoryEvent.product_area == product_area)
    if technology:
        query = query.filter(MemoryEvent.technology == technology)
    return query.order_by(MemoryEvent.date.desc()).all()

@router.get("/insights")
def get_memory_insights(db: Session = Depends(get_db)):
    total = db.query(MemoryEvent).count()
    fb = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "FEEDBACK").count()
    pd = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "PRODUCT_DECISION").count()
    ed = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "ENGINEERING_DECISION").count()
    ad = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "ARCHITECTURE_DECISION").count()
    rej = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "ALTERNATIVE_REJECTED").count()
    out = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "OUTCOME").count()
    les = db.query(MemoryEvent).filter(MemoryEvent.memory_type == "LESSON").count()

    return {
        "total_memories": total,
        "counts_by_type": {
            "FEEDBACK": fb,
            "PRODUCT_DECISION": pd,
            "ENGINEERING_DECISION": ed,
            "ARCHITECTURE_DECISION": ad,
            "ALTERNATIVE_REJECTED": rej,
            "OUTCOME": out,
            "LESSON": les
        }
    }

@router.get("/status", response_model=HindsightStatusRead)
def get_hindsight_status(db: Session = Depends(get_db)):
    status = hindsight_service.check_status()
    total = db.query(MemoryEvent).count()
    status["total_memories_retained"] = total
    return status
