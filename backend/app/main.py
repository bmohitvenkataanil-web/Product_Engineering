import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routes import (
    feedback, product_decisions, engineering_decisions,
    architecture_decisions, experiments, outcomes, agent,
    memory, timeline, demo
)
from app.seed.demo_data import seed_demo_data
from app.models.models import Feedback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("decision_memory_app")

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Decision Memory API",
    description="Organizational memory system connecting customer feedback, product decisions, engineering decisions, and outcomes with Hindsight by Vectorize.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(feedback.router)
app.include_router(product_decisions.router)
app.include_router(engineering_decisions.router)
app.include_router(architecture_decisions.router)
app.include_router(experiments.router)
app.include_router(outcomes.router)
app.include_router(agent.router)
app.include_router(memory.router)
app.include_router(timeline.router)
app.include_router(demo.router)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        fb_count = db.query(Feedback).count()
        if fb_count == 0:
            logger.info("Empty database detected on startup. Auto-seeding 60-80 demo events...")
            seed_demo_data(db)
        else:
            logger.info(f"Database ready with {fb_count} feedback records.")
    except Exception as e:
        logger.error(f"Startup database check/seed error: {e}")
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "name": "Decision Memory API",
        "status": "online",
        "tagline": "Remember what your organization decided, why it decided it, and what happened afterward.",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
