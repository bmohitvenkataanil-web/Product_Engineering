#!/usr/bin/env python3
"""
CLI script to seed Decision Memory demo dataset.
Populates PostgreSQL database and Hindsight Memory Bank with 60-80 interconnected events across 5 core stories.
"""
import sys
import os

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.database import SessionLocal
from app.seed.demo_data import seed_demo_data

def main():
    print("=========================================================")
    print("  Decision Memory - Synthetic Demo Seed Generator")
    print("=========================================================")
    db = SessionLocal()
    try:
        res = seed_demo_data(db)
        print("\nSeed Process Complete!")
        print(f"- Feedback Events: {res['feedback_count']}")
        print(f"- Product Decisions: {res['product_decisions_count']}")
        print(f"- Engineering ADRs: {res['engineering_decisions_count']}")
        print(f"- Architecture Decisions: {res['architecture_decisions_count']}")
        print(f"- Experiments: {res['experiments_count']}")
        print(f"- Measured Outcomes: {res['outcomes_count']}")
        print(f"- Retained Memory Events: {res['retained_memory_events_count']}")
        print("=========================================================")
    finally:
        db.close()

if __name__ == "__main__":
    main()
