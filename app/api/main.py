from datetime import datetime, timezone
from fastapi import FastAPI
import random
import time

app = FastAPI(
    title="Chaos Engineering Sandbox API",
    description="A simple API used to test health checks, readiness, observability, and chaos engineering experiments.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Chaos Engineering Sandbox API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "chaos-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready")
def readiness_check():
    return {
        "status": "ready",
        "service": "chaos-api",
        "dependencies": {
            "database": "not_configured_yet",
            "cache": "not_configured_yet",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/status")
def service_status():
    return {
        "service": "chaos-api",
        "version": "0.1.0",
        "environment": "local",
        "status": "running",
        "features": {
            "database": False,
            "cache": False,
            "observability": False,
            "chaos_experiments": False,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/simulate-work")
def simulate_work():
    processing_time = round(random.uniform(0.1, 1.5), 2)
    time.sleep(processing_time)

    return {
        "message": "Work simulation completed",
        "processing_time_seconds": processing_time,
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }