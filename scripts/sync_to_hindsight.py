#!/usr/bin/env python3
"""
Real Data Sync Script for Hindsight Memory Bank.
Pushes all database records (Feedbacks, Product Decisions, Engineering ADRs, Outcomes)
directly to your live Hindsight API endpoint and Bank ID.
"""
import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.database import SessionLocal
from app.config import settings
from app.models.models import Feedback, ProductDecision, EngineeringDecision, ArchitectureDecision, Outcome, Experiment
from app.services.hindsight import hindsight_service
from app.services.decision_memory import memory_manager

def main():
    print("=================================================================")
    print("   Hindsight API - Live Real Data Synchronization Pipeline      ")
    print("=================================================================")
    print(f"Target Hindsight Base URL : {settings.HINDSIGHT_BASE_URL}")
    print(f"Target Hindsight Bank ID  : {settings.HINDSIGHT_BANK_ID}")
    print(f"Hindsight API Key Status  : {'Configured' if settings.HINDSIGHT_API_KEY else 'UNSET (Local Fallback Mode)'}")
    print("-----------------------------------------------------------------")

    db = SessionLocal()
    total_synced = 0

    try:
        # 1. Sync Feedback
        feedbacks = db.query(Feedback).all()
        print(f"[*] Retaining {len(feedbacks)} Customer Feedback items to Hindsight...")
        for fb in feedbacks:
            memory_manager.retain_feedback_experience(db, fb)
            total_synced += 1

        # 2. Sync Product Decisions
        pds = db.query(ProductDecision).all()
        print(f"[*] Retaining {len(pds)} Product Decision items to Hindsight...")
        for pd in pds:
            memory_manager.retain_product_decision_experience(db, pd)
            total_synced += 1

        # 3. Sync Engineering ADRs
        eds = db.query(EngineeringDecision).all()
        print(f"[*] Retaining {len(eds)} Engineering ADR items to Hindsight...")
        for ed in eds:
            memory_manager.retain_engineering_decision_experience(db, ed)
            total_synced += 1

        # 4. Sync Outcomes
        outcomes = db.query(Outcome).all()
        print(f"[*] Retaining {len(outcomes)} Measured Outcomes to Hindsight...")
        for out in outcomes:
            memory_manager.retain_outcome_experience(db, out)
            total_synced += 1

        print("-----------------------------------------------------------------")
        print(f"SUCCESS! Synchronized {total_synced} real experience records to Hindsight Bank '{settings.HINDSIGHT_BANK_ID}'.")
        print("=================================================================")

    finally:
        db.close()

if __name__ == "__main__":
    main()
