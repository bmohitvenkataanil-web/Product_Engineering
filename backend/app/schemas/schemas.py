from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

# Feedback Schemas
class FeedbackCreate(BaseModel):
    customer_id: Optional[str] = None
    customer_name: str
    content: str
    product_area: str
    sentiment: Optional[str] = "Neutral"
    priority: Optional[str] = "Medium"
    date: str
    status: Optional[str] = "Open"

class FeedbackRead(FeedbackCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

class FeedbackAnalyzeResponse(BaseModel):
    feedback_id: str
    problem: str
    historical_evidence: List[Dict[str, Any]]
    previous_attempts: List[str]
    observed_outcome: str
    recommendation: str
    trade_offs: str
    next_step: str
    memory_confidence: str # Strong, Moderate, Limited, None
    memory_mode_used: str # ON, OFF

# Product Decision Schemas
class ProductDecisionCreate(BaseModel):
    title: str
    problem: str
    context: Optional[str] = None
    options_considered: List[str] = []
    chosen_approach: str
    reason: str
    expected_outcome: Optional[str] = None
    actual_outcome: Optional[str] = None
    date: str
    status: Optional[str] = "Accepted"
    product_area: str
    related_feedback_id: Optional[str] = None

class ProductDecisionRead(ProductDecisionCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Engineering Decision Schemas
class AlternativeOption(BaseModel):
    name: str
    reason_rejected: Optional[str] = None

class EngineeringDecisionCreate(BaseModel):
    title: str
    problem: str
    context: Optional[str] = None
    decision: str
    alternatives_considered: List[str] = []
    rejected_alternatives: List[AlternativeOption] = []
    constraints: Optional[str] = None
    trade_offs: Optional[str] = None
    expected_consequences: Optional[str] = None
    actual_consequences: Optional[str] = None
    technology: str
    architecture_area: str
    date: str
    status: Optional[str] = "Accepted"
    related_product_decision_id: Optional[str] = None
    related_feedback_id: Optional[str] = None

class EngineeringDecisionRead(EngineeringDecisionCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Architecture Decision Schemas
class ArchitectureDecisionCreate(BaseModel):
    title: str
    status: Optional[str] = "Accepted"
    date: str
    technology: str
    problem: str
    context: Optional[str] = None
    constraints: Optional[str] = None
    options: List[str] = []
    decision: str
    trade_offs: Optional[str] = None
    consequences: Optional[str] = None
    related_decisions: List[str] = []

class ArchitectureDecisionRead(ArchitectureDecisionCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Experiment Schemas
class ExperimentCreate(BaseModel):
    name: str
    product_area: str
    hypothesis: str
    variant_a: str
    variant_b: str
    start_date: str
    end_date: Optional[str] = None
    result: Optional[str] = None
    conclusion: Optional[str] = None
    status: Optional[str] = "Running"

class ExperimentCompleteRequest(BaseModel):
    end_date: str
    result: str
    conclusion: str
    status: str = "Completed"

class ExperimentRead(ExperimentCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Outcome Schemas
class OutcomeCreate(BaseModel):
    title: str
    description: str
    category: Optional[str] = "Product Performance"
    metrics_impact: Optional[str] = None
    date: str
    related_decision_type: Optional[str] = None
    related_decision_id: Optional[str] = None

class OutcomeRead(OutcomeCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# AI Advisor Request & Response
class AdviceRequest(BaseModel):
    question: str
    domain: Optional[str] = "Both" # Product, Engineering, Both
    memory_mode: Optional[str] = "ON" # ON, OFF

class HistoricalEvidenceItem(BaseModel):
    type: str # Engineering Decision, Product Decision, Rejected Alternative, Outcome, Feedback, Lesson
    date: str
    title: str
    summary: str
    relevance_reason: str

class AdviceResponse(BaseModel):
    question: str
    domain: str
    memory_mode: str
    recommendation: str
    historical_context: Optional[str] = None
    previous_decisions: List[str] = []
    alternatives_rejected: List[Dict[str, str]] = []
    trade_offs: Optional[str] = None
    observed_outcomes: Optional[str] = None
    what_changed: Optional[str] = None
    suggested_next_step: Optional[str] = None
    relevant_memories: List[HistoricalEvidenceItem] = []
    memory_confidence: str # Strong, Moderate, Limited, None
    memory_status: str # Connected, Unavailable, Offline

class CompareAdviceResponse(BaseModel):
    question: str
    without_memory: AdviceResponse
    with_memory: AdviceResponse
    what_changed_summary: str

# Memory & Hindsight Schemas
class RetainMemoryRequest(BaseModel):
    memory_type: str
    summary: str
    content: str
    product_area: Optional[str] = None
    technology: Optional[str] = None
    date: str
    related_decision_id: Optional[str] = None
    related_outcome_id: Optional[str] = None

class RecallMemoryRequest(BaseModel):
    query: str
    bank_id: Optional[str] = None
    top_k: Optional[int] = 5

class ReflectMemoryRequest(BaseModel):
    query: str
    bank_id: Optional[str] = None

class MemoryEventRead(RetainMemoryRequest):
    id: str
    hindsight_memory_id: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class TimelineEventRead(BaseModel):
    id: str
    date: str
    type: str # Problem, Product Decision, Engineering Decision, Implementation, Outcome, Experiment, Lesson
    title: str
    description: str
    product_area: Optional[str] = None
    technology: Optional[str] = None
    status: Optional[str] = None
    related_id: Optional[str] = None

class HindsightStatusRead(BaseModel):
    connected: bool
    mode: str # Cloud, Local, Fallback
    bank_id: str
    base_url: str
    total_memories_retained: int
    message: str
