from datetime import datetime, timezone
import os
import random
import time

import psycopg
import redis
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)


app = FastAPI(
    title="Chaos Engineering Sandbox API",
    description="A simple API used to test health checks, readiness, observability, and chaos engineering experiments.",
    version="0.3.0",
)


REQUEST_COUNT = Counter(
    "chaos_api_http_requests_total",
    "Total number of HTTP requests received by the Chaos API",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "chaos_api_http_request_duration_seconds",
    "HTTP request latency in seconds for the Chaos API",
    ["method", "endpoint"],
)

DEPENDENCY_UP = Gauge(
    "chaos_api_dependency_up",
    "Dependency health status where 1 means reachable and 0 means unreachable",
    ["dependency"],
)

IN_PROGRESS_REQUESTS = Gauge(
    "chaos_api_http_requests_in_progress",
    "Number of HTTP requests currently being processed by the Chaos API",
)


def utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method

    if endpoint == "/metrics":
        return await call_next(request)

    IN_PROGRESS_REQUESTS.inc()
    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        return response
    except Exception:
        status_code = "500"
        raise
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            http_status=status_code,
        ).inc()
        IN_PROGRESS_REQUESTS.dec()


def check_postgres():
    try:
        connection = psycopg.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "chaosdb"),
            user=os.getenv("POSTGRES_USER", "chaosuser"),
            password=os.getenv("POSTGRES_PASSWORD", "chaospassword"),
            connect_timeout=2,
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        cursor.close()
        connection.close()
        return {"status": "reachable", "message": "PostgreSQL connection successful"}
    except Exception as error:
        return {"status": "unreachable", "message": str(error)}


def check_redis():
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()
        return {"status": "reachable", "message": "Redis connection successful"}
    except Exception as error:
        return {"status": "unreachable", "message": str(error)}


@app.get("/")
def root():
    return {
        "message": "Chaos Engineering Sandbox API",
        "status": "running",
        "docs": "/docs",
        "metrics": "/metrics",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "chaos-api",
        "timestamp": utc_timestamp(),
    }


@app.get("/ready")
def readiness_check():
    postgres_status = check_postgres()
    redis_status = check_redis()

    DEPENDENCY_UP.labels(dependency="postgres").set(
        1 if postgres_status["status"] == "reachable" else 0
    )

    DEPENDENCY_UP.labels(dependency="redis").set(
        1 if redis_status["status"] == "reachable" else 0
    )

    is_ready = (
        postgres_status["status"] == "reachable"
        and redis_status["status"] == "reachable"
    )

    return {
        "status": "ready" if is_ready else "not_ready",
        "service": "chaos-api",
        "dependencies": {
            "database": postgres_status,
            "cache": redis_status,
        },
        "timestamp": utc_timestamp(),
    }


@app.get("/status")
def service_status():
    postgres_status = check_postgres()
    redis_status = check_redis()

    return {
        "service": "chaos-api",
        "version": "0.3.0",
        "environment": os.getenv("APP_ENV", "local"),
        "status": "running",
        "features": {
            "database": postgres_status["status"] == "reachable",
            "cache": redis_status["status"] == "reachable",
            "observability": True,
            "chaos_experiments": True,
        },
        "dependencies": {
            "database": postgres_status,
            "cache": redis_status,
        },
        "timestamp": utc_timestamp(),
    }


@app.get("/simulate-work")
def simulate_work(delay: float = 0.2):
    safe_delay = min(max(delay, 0), 5)

    time.sleep(safe_delay)

    return {
        "status": "success",
        "message": "Work simulation completed",
        "processing_time_seconds": safe_delay,
        "delay_seconds": safe_delay,
        "timestamp": utc_timestamp(),
    }

@app.get("/simulate-error")
def simulate_error():
    raise HTTPException(
        status_code=500,
        detail="Simulated API error for alert validation",
    )


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )