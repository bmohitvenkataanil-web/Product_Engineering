from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=True)
    tier = Column(String, default="Enterprise")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ProductVersion(Base):
    __tablename__ = "product_versions"

    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"))
    version_str = Column(String, nullable=False)
    release_date = Column(String, nullable=True)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=True)
    customer_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    product_area = Column(String, nullable=False, index=True)
    sentiment = Column(String, default="Neutral") # Negative, Neutral, Positive
    priority = Column(String, default="Medium") # Low, Medium, High, Critical
    date = Column(String, nullable=False)
    status = Column(String, default="Open") # Open, Under Review, Addressed, Deferred
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ProductDecision(Base):
    __tablename__ = "product_decisions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    problem = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    options_considered = Column(JSON, default=list)
    chosen_approach = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    expected_outcome = Column(Text, nullable=True)
    actual_outcome = Column(Text, nullable=True)
    date = Column(String, nullable=False)
    status = Column(String, default="Accepted") # Proposed, Accepted, Implemented, Superseded
    product_area = Column(String, nullable=False, index=True)
    related_feedback_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EngineeringDecision(Base):
    __tablename__ = "engineering_decisions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    problem = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    decision = Column(Text, nullable=False)
    alternatives_considered = Column(JSON, default=list)
    rejected_alternatives = Column(JSON, default=list)
    constraints = Column(Text, nullable=True)
    trade_offs = Column(Text, nullable=True)
    expected_consequences = Column(Text, nullable=True)
    actual_consequences = Column(Text, nullable=True)
    technology = Column(String, nullable=False, index=True)
    architecture_area = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)
    status = Column(String, default="Accepted")
    related_product_decision_id = Column(String, nullable=True)
    related_feedback_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ArchitectureDecision(Base):
    __tablename__ = "architecture_decisions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="Accepted")
    date = Column(String, nullable=False)
    technology = Column(String, nullable=False, index=True)
    problem = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    constraints = Column(Text, nullable=True)
    options = Column(JSON, default=list)
    decision = Column(Text, nullable=False)
    trade_offs = Column(Text, nullable=True)
    consequences = Column(Text, nullable=True)
    related_decisions = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    product_area = Column(String, nullable=False)
    hypothesis = Column(Text, nullable=False)
    variant_a = Column(Text, nullable=False)
    variant_b = Column(Text, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=True)
    result = Column(Text, nullable=True)
    conclusion = Column(Text, nullable=True)
    status = Column(String, default="Running") # Running, Completed, Inconclusive, Cancelled
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, default="Product Performance") # Product Performance, Technical Latency, Operational Cost, User Satisfaction
    metrics_impact = Column(String, nullable=True)
    date = Column(String, nullable=False)
    related_decision_type = Column(String, nullable=True) # ProductDecision, EngineeringDecision, ArchitectureDecision, Experiment
    related_decision_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AgentRecommendation(Base):
    __tablename__ = "agent_recommendations"

    id = Column(String, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    domain = Column(String, default="Both") # Product, Engineering, Both
    memory_mode = Column(String, default="ON") # ON, OFF
    recommendation = Column(Text, nullable=False)
    historical_context = Column(Text, nullable=True)
    previous_decisions = Column(JSON, default=list)
    alternatives_rejected = Column(JSON, default=list)
    trade_offs = Column(Text, nullable=True)
    observed_outcomes = Column(Text, nullable=True)
    what_changed = Column(Text, nullable=True)
    suggested_next_step = Column(Text, nullable=True)
    relevant_memories = Column(JSON, default=list)
    memory_confidence = Column(String, default="Strong") # Strong, Moderate, Limited, None
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class MemoryEvent(Base):
    __tablename__ = "memory_events"

    id = Column(String, primary_key=True, index=True)
    memory_type = Column(String, nullable=False, index=True) # FEEDBACK, PRODUCT_DECISION, ENGINEERING_DECISION, ARCHITECTURE_DECISION, ALTERNATIVE_REJECTED, OUTCOME, LESSON
    summary = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    product_area = Column(String, nullable=True, index=True)
    technology = Column(String, nullable=True, index=True)
    hindsight_memory_id = Column(String, nullable=True)
    date = Column(String, nullable=False)
    related_decision_id = Column(String, nullable=True)
    related_outcome_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DecisionRelationship(Base):
    __tablename__ = "decision_relationships"

    id = Column(String, primary_key=True, index=True)
    source_type = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    relationship_type = Column(String, nullable=False) # MOTIVATED_BY, LEADS_TO, REJECTED_IN_FAVOR_OF, RESULTED_IN, LESSON_FROM
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TechnologyArea(Base):
    __tablename__ = "technology_areas"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
