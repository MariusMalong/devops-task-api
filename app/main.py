from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import engine, Base
from app.routers import auth, tasks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management Microservice API",
    description="Production-grade REST API supporting DevOps pipeline automation.",
    version="1.0.0",
)

# Instrument Prometheus Metrics for Stage 7 Monitoring
Instrumentator().instrument(app).expose(app)

# Include Routers
app.include_router(auth.router)
app.include_router(tasks.router)

# hello world

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Health check endpoint for container probes and monitoring."""
    return {"status": "healthy", "service": "task-management-api", "version": "1.0.0"}