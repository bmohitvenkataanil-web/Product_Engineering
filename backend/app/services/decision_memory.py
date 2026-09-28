from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.models import MemoryEvent, Feedback, ProductDecision, EngineeringDecision, ArchitectureDecision, Experiment, Outcome, DecisionRelationship
from app.services.hindsight import hindsight_service

class DecisionMemoryManager:
    """
    Manages the organizational memory lifecycle:
    - Extracting durable organizational experiences from decisions/feedback/outcomes
    - Retaining experiences into Hindsight memory bank & PostgreSQL memory events
    - Searching and retrieving historical evidence for grounding decision recommendations
    """

    @staticmethod
    def retain_feedback_experience(db: Session, feedback: Feedback) -> MemoryEvent:
        summary = f"Customer Feedback [{feedback.customer_name}]: {feedback.content[:80]}..."
        content = (
            f"Customer '{feedback.customer_name}' reported feedback in product area '{feedback.product_area}' "
            f"(Sentiment: {feedback.sentiment}, Priority: {feedback.priority}) on {feedback.date}: "
            f"\"{feedback.content}\""
        )
        metadata = {
            "memory_type": "FEEDBACK",
            "product_area": feedback.product_area,
            "date": feedback.date,
            "feedback_id": feedback.id
        }

        # Retain in Hindsight
        hindsight_res = hindsight_service.retain(content=content, metadata=metadata)

        mem_event = MemoryEvent(
            id=f"MEM-FB-{feedback.id}",
            memory_type="FEEDBACK",
            summary=summary,
            content=content,
            product_area=feedback.product_area,
            technology=None,
            hindsight_memory_id=hindsight_res.get("hindsight_id"),
            date=feedback.date,
            related_decision_id=None,
            related_outcome_id=None
        )
        db.merge(mem_event)
        db.commit()
        return mem_event

    @staticmethod
    def retain_product_decision_experience(db: Session, decision: ProductDecision) -> MemoryEvent:
        options_str = ", ".join(decision.options_considered) if decision.options_considered else "N/A"
        summary = f"Product Decision [{decision.product_area}]: {decision.title}"
        content = (
            f"Product Decision ({decision.id}) on {decision.date} for product area '{decision.product_area}':\n"
            f"Title: {decision.title}\n"
            f"Problem: {decision.problem}\n"
            f"Context: {decision.context or 'N/A'}\n"
            f"Options Considered: {options_str}\n"
            f"Chosen Approach: {decision.chosen_approach}\n"
            f"Reasoning: {decision.reason}\n"
            f"Expected Outcome: {decision.expected_outcome or 'N/A'}\n"
            f"Actual Outcome: {decision.actual_outcome or 'Pending'}"
        )
        metadata = {
            "memory_type": "PRODUCT_DECISION",
            "product_area": decision.product_area,
            "date": decision.date,
            "decision_id": decision.id
        }

        hindsight_res = hindsight_service.retain(content=content, metadata=metadata)

        mem_event = MemoryEvent(
            id=f"MEM-PD-{decision.id}",
            memory_type="PRODUCT_DECISION",
            summary=summary,
            content=content,
            product_area=decision.product_area,
            technology=None,
            hindsight_memory_id=hindsight_res.get("hindsight_id"),
            date=decision.date,
            related_decision_id=decision.id,
            related_outcome_id=None
        )
        db.merge(mem_event)
        db.commit()
        return mem_event

    @staticmethod
    def retain_engineering_decision_experience(db: Session, decision: EngineeringDecision) -> MemoryEvent:
        alts_str = ", ".join(decision.alternatives_considered) if decision.alternatives_considered else "N/A"
        rejected_str = ""
        if decision.rejected_alternatives:
            rejected_items = []
            for alt in decision.rejected_alternatives:
                if isinstance(alt, dict):
                    name = alt.get("name", "")
                    reason = alt.get("reason_rejected", "No reason recorded")
                    rejected_items.append(f"{name} (Reason: {reason})")
                else:
                    rejected_items.append(str(alt))
            rejected_str = "; ".join(rejected_items)
        else:
            rejected_str = "None explicitly recorded"

        summary = f"Engineering Decision [{decision.technology}]: {decision.title}"
        content = (
            f"Engineering Decision ADR ({decision.id}) on {decision.date} for area '{decision.architecture_area}':\n"
            f"Title: {decision.title}\n"
            f"Technology: {decision.technology}\n"
            f"Problem: {decision.problem}\n"
            f"Context: {decision.context or 'N/A'}\n"
            f"Decision Made: {decision.decision}\n"
            f"Alternatives Evaluated: {alts_str}\n"
            f"Rejected Alternatives & Reasons: {rejected_str}\n"
            f"Constraints: {decision.constraints or 'N/A'}\n"
            f"Trade-offs: {decision.trade_offs or 'N/A'}\n"
            f"Expected Consequences: {decision.expected_consequences or 'N/A'}\n"
            f"Actual Consequences: {decision.actual_consequences or 'Pending'}"
        )
        metadata = {
            "memory_type": "ENGINEERING_DECISION",
            "technology": decision.technology,
            "architecture_area": decision.architecture_area,
            "date": decision.date,
            "decision_id": decision.id
        }

        hindsight_res = hindsight_service.retain(content=content, metadata=metadata)

        mem_event = MemoryEvent(
            id=f"MEM-ED-{decision.id}",
            memory_type="ENGINEERING_DECISION",
            summary=summary,
            content=content,
            product_area=decision.architecture_area,
            technology=decision.technology,
            hindsight_memory_id=hindsight_res.get("hindsight_id"),
            date=decision.date,
            related_decision_id=decision.id,
            related_outcome_id=None
        )
        db.merge(mem_event)

        # If rejected alternatives exist, retain them as distinct memory events for quick recall
        if decision.rejected_alternatives:
            for idx, alt in enumerate(decision.rejected_alternatives):
                alt_name = alt.get("name") if isinstance(alt, dict) else str(alt)
                alt_reason = alt.get("reason_rejected") if isinstance(alt, dict) else "Not selected"
                rej_content = f"Rejected Alternative: In decision '{decision.title}' on {decision.date}, '{alt_name}' was rejected. Reason: {alt_reason}. Constraints: {decision.constraints}"
                rej_mem = MemoryEvent(
                    id=f"MEM-REJ-{decision.id}-{idx}",
                    memory_type="ALTERNATIVE_REJECTED",
                    summary=f"Rejected Alternative [{decision.technology}]: {alt_name} rejected for {decision.title}",
                    content=rej_content,
                    product_area=decision.architecture_area,
                    technology=decision.technology,
                    hindsight_memory_id=None,
                    date=decision.date,
                    related_decision_id=decision.id,
                    related_outcome_id=None
                )
                db.merge(rej_mem)
                hindsight_service.retain(content=rej_content, metadata={"memory_type": "ALTERNATIVE_REJECTED", "technology": decision.technology})

        db.commit()
        return mem_event

    @staticmethod
    def retain_outcome_experience(db: Session, outcome: Outcome) -> MemoryEvent:
        summary = f"Outcome [{outcome.category}]: {outcome.title}"
        content = (
            f"Measured Outcome ({outcome.id}) on {outcome.date}:\n"
            f"Title: {outcome.title}\n"
            f"Category: {outcome.category}\n"
            f"Description: {outcome.description}\n"
            f"Metrics Impact: {outcome.metrics_impact or 'N/A'}\n"
            f"Related Decision: {outcome.related_decision_type} #{outcome.related_decision_id or 'N/A'}"
        )
        metadata = {
            "memory_type": "OUTCOME",
            "category": outcome.category,
            "date": outcome.date,
            "outcome_id": outcome.id
        }

        hindsight_res = hindsight_service.retain(content=content, metadata=metadata)

        mem_event = MemoryEvent(
            id=f"MEM-OUT-{outcome.id}",
            memory_type="OUTCOME",
            summary=summary,
            content=content,
            product_area=None,
            technology=None,
            hindsight_memory_id=hindsight_res.get("hindsight_id"),
            date=outcome.date,
            related_decision_id=outcome.related_decision_id,
            related_outcome_id=outcome.id
        )
        db.merge(mem_event)

        # Retain lesson learned
        lesson_content = f"Lesson Learned from Outcome '{outcome.title}': {outcome.description}. Measured impact: {outcome.metrics_impact}."
        lesson_mem = MemoryEvent(
            id=f"MEM-LES-{outcome.id}",
            memory_type="LESSON",
            summary=f"Lesson: {outcome.title}",
            content=lesson_content,
            product_area=None,
            technology=None,
            hindsight_memory_id=None,
            date=outcome.date,
            related_decision_id=outcome.related_decision_id,
            related_outcome_id=outcome.id
        )
        db.merge(lesson_mem)
        hindsight_service.retain(content=lesson_content, metadata={"memory_type": "LESSON", "date": outcome.date})

        db.commit()
        return mem_event

    @staticmethod
    def search_local_memories(db: Session, query: str, limit: int = 8) -> List[MemoryEvent]:
        """Query structured PostgreSQL memory events with keyword matching."""
        terms = [t.lower() for t in query.split() if len(t) > 2]
        all_events = db.query(MemoryEvent).order_by(MemoryEvent.date.desc()).all()

        if not terms:
            return all_events[:limit]

        scored = []
        for event in all_events:
            text = (f"{event.summary} {event.content} {event.product_area or ''} {event.technology or ''}").lower()
            score = sum(1 for term in terms if term in text)
            if score > 0:
                scored.append((score, event))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

memory_manager = DecisionMemoryManager()
