from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.seed.demo_data import seed_demo_data
from app.services.analytics import analytics_service

router = APIRouter(prefix="/api/demo", tags=["Demo & Data Management"])

@router.post("/load")
def load_demo_data(db: Session = Depends(get_db)):
    result = seed_demo_data(db)
    return {"message": "Demo data loaded successfully", "details": result}

@router.post("/reset")
def reset_demo_data(db: Session = Depends(get_db)):
    result = seed_demo_data(db)
    return {"message": "Demo dataset reset to baseline state", "details": result}

@router.post("/clear")
def clear_all_data(db: Session = Depends(get_db)):
    """Wipes all database tables to start fresh with real company data."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "All database tables cleared. System ready for real company data."}

@router.get("/dashboard")
def get_dashboard_analytics(db: Session = Depends(get_db)):
    return analytics_service.get_dashboard_data(db)
