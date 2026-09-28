from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Experiment
from app.schemas.schemas import ExperimentCreate, ExperimentCompleteRequest, ExperimentRead
from app.services.decision_memory import memory_manager
from app.services.hindsight import hindsight_service

router = APIRouter(prefix="/api/experiments", tags=["Experiments"])

@router.post("", response_model=ExperimentRead)
def create_experiment(exp_in: ExperimentCreate, db: Session = Depends(get_db)):
    exp_count = db.query(Experiment).count()
    exp_id = f"EXP-{508 + exp_count}"

    exp = Experiment(
        id=exp_id,
        name=exp_in.name,
        product_area=exp_in.product_area,
        hypothesis=exp_in.hypothesis,
        variant_a=exp_in.variant_a,
        variant_b=exp_in.variant_b,
        start_date=exp_in.start_date,
        end_date=exp_in.end_date,
        result=exp_in.result,
        conclusion=exp_in.conclusion,
        status=exp_in.status or "Running"
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@router.get("", response_model=List[ExperimentRead])
def get_experiments(
    product_area: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Experiment)
    if product_area:
        query = query.filter(Experiment.product_area == product_area)
    if status:
        query = query.filter(Experiment.status == status)
    return query.order_by(Experiment.start_date.desc()).all()

@router.get("/{experiment_id}", response_model=ExperimentRead)
def get_experiment_detail(experiment_id: str, db: Session = Depends(get_db)):
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.post("/{experiment_id}/complete", response_model=ExperimentRead)
def complete_experiment(
    experiment_id: str,
    complete_in: ExperimentCompleteRequest,
    db: Session = Depends(get_db)
):
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    exp.end_date = complete_in.end_date
    exp.result = complete_in.result
    exp.conclusion = complete_in.conclusion
    exp.status = complete_in.status or "Completed"

    db.commit()
    db.refresh(exp)

    # Retain experiment outcome experience in Hindsight
    exp_content = (
        f"Completed Experiment '{exp.name}' ({exp.id}) in area '{exp.product_area}' on {exp.end_date}:\n"
        f"Hypothesis: {exp.hypothesis}\n"
        f"Result: {exp.result}\n"
        f"Conclusion & Lesson: {exp.conclusion}"
    )
    hindsight_service.retain(content=exp_content, metadata={"memory_type": "EXPERIMENT_RESULT", "product_area": exp.product_area})

    return exp
