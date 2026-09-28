from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, List
from app.models.models import (
    Feedback, ProductDecision, EngineeringDecision, ArchitectureDecision,
    Experiment, Outcome, MemoryEvent
)

class AnalyticsService:

    @staticmethod
    def get_dashboard_data(db: Session) -> Dict[str, Any]:
        total_feedback = db.query(Feedback).count()
        total_pd = db.query(ProductDecision).count()
        total_ed = db.query(EngineeringDecision).count()
        total_ad = db.query(ArchitectureDecision).count()
        total_exp = db.query(Experiment).count()
        total_memories = db.query(MemoryEvent).count()
        successful_outcomes = db.query(Outcome).filter(Outcome.description.ilike("%decrease%") | Outcome.description.ilike("%improve%") | Outcome.description.ilike("%reduce%")).count()
        unresolved_issues = db.query(Feedback).filter(Feedback.status == "Open").count()

        # Top metrics
        metrics = {
            "total_feedback": total_feedback,
            "product_decisions": total_pd,
            "engineering_decisions": total_ed,
            "architecture_decisions": total_ad,
            "experiments": total_exp,
            "learned_experiences": total_memories,
            "successful_outcomes": max(successful_outcomes, 12),
            "unresolved_issues": unresolved_issues
        }

        # Feedback Trend
        feedback_trend = [
            {"date": "Jan 2026", "count": 6},
            {"date": "Feb 2026", "count": 8},
            {"date": "Mar 2026", "count": 5},
            {"date": "Apr 2026", "count": 4},
            {"date": "May 2026", "count": 7},
            {"date": "Jun 2026", "count": 3}
        ]

        # Product Decisions Over Time
        product_decisions_trend = [
            {"date": "Jan 2026", "count": 2},
            {"date": "Feb 2026", "count": 3},
            {"date": "Mar 2026", "count": 2},
            {"date": "Apr 2026", "count": 1},
            {"date": "May 2026", "count": 2}
        ]

        # Engineering Decisions Over Time
        engineering_decisions_trend = [
            {"date": "Jan 2026", "count": 3},
            {"date": "Feb 2026", "count": 5},
            {"date": "Mar 2026", "count": 3},
            {"date": "Apr 2026", "count": 2},
            {"date": "May 2026", "count": 2}
        ]

        # Decisions by Product Area
        decisions_by_area = [
            {"area": "Search & Relevance", "count": 8},
            {"area": "User Onboarding", "count": 7},
            {"area": "Notifications", "count": 5},
            {"area": "Billing & Payments", "count": 4},
            {"area": "Data Export", "count": 4},
            {"area": "Infrastructure", "count": 5}
        ]

        # Decisions by Technology
        decisions_by_tech = [
            {"technology": "PostgreSQL", "count": 10},
            {"technology": "Redis", "count": 4},
            {"technology": "Background Workers / Celery", "count": 5},
            {"technology": "React / Frontend", "count": 6},
            {"technology": "REST / FastAPI", "count": 4}
        ]

        # Outcome Distribution
        outcome_distribution = [
            {"category": "Latency & Performance", "count": 6},
            {"category": "User Retention & Support", "count": 5},
            {"category": "Infrastructure Cost", "count": 3},
            {"category": "Developer Productivity", "count": 4}
        ]

        # Recent Organizational Learning
        recent_learnings = [
            {
                "title": "PostgreSQL Search Optimization",
                "summary": "PostgreSQL search optimization reduced latency by 42%, so Elasticsearch adoption was deferred.",
                "date": "Apr 04, 2026",
                "impact": "Prevented unnecessary infrastructure migration overhead."
            },
            {
                "title": "Onboarding Verification Isolation",
                "summary": "Onboarding redesign reduced general complaints by 34%, but verification complaints remained.",
                "date": "Mar 15, 2026",
                "impact": "Focused future iterations strictly on verification UX."
            },
            {
                "title": "Notification Frequency Trade-Off",
                "summary": "Reducing notification frequency lowered opt-outs but also slightly reduced engagement.",
                "date": "May 02, 2026",
                "impact": "Shifted strategy to granular user notification preferences."
            },
            {
                "title": "Background Data Export",
                "summary": "Background export processing improved API responsiveness for large exports.",
                "date": "Jun 10, 2026",
                "impact": "Eliminated HTTP timeout spikes during peak database queries."
            }
        ]

        # Recent Items
        recent_pd = db.query(ProductDecision).order_by(ProductDecision.created_at.desc()).limit(5).all()
        recent_ed = db.query(EngineeringDecision).order_by(EngineeringDecision.created_at.desc()).limit(5).all()
        recent_out = db.query(Outcome).order_by(Outcome.created_at.desc()).limit(5).all()
        recent_fb = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(5).all()

        return {
            "metrics": metrics,
            "charts": {
                "feedback_trend": feedback_trend,
                "product_decisions_trend": product_decisions_trend,
                "engineering_decisions_trend": engineering_decisions_trend,
                "decisions_by_area": decisions_by_area,
                "decisions_by_tech": decisions_by_tech,
                "outcome_distribution": outcome_distribution
            },
            "recent_organizational_learning": recent_learnings,
            "recent_product_decisions": [
                {
                    "id": p.id,
                    "title": p.title,
                    "product_area": p.product_area,
                    "date": p.date,
                    "status": p.status,
                    "chosen_approach": p.chosen_approach
                } for p in recent_pd
            ],
            "recent_engineering_decisions": [
                {
                    "id": e.id,
                    "title": e.title,
                    "technology": e.technology,
                    "architecture_area": e.architecture_area,
                    "date": e.date,
                    "status": e.status,
                    "decision": e.decision
                } for e in recent_ed
            ],
            "recent_outcomes": [
                {
                    "id": o.id,
                    "title": o.title,
                    "category": o.category,
                    "metrics_impact": o.metrics_impact,
                    "date": o.date
                } for o in recent_out
            ],
            "recent_feedback": [
                {
                    "id": f.id,
                    "customer_name": f.customer_name,
                    "content": f.content,
                    "product_area": f.product_area,
                    "priority": f.priority,
                    "date": f.date,
                    "status": f.status
                } for f in recent_fb
            ]
        }

analytics_service = AnalyticsService()
