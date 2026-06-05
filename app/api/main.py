from datetime import datetime, timezone
import os
import random
import time

import psycopg
import redis
from fastapi import FastAPI


app = FastAPI(
    title="Chaos Engineering Sandbox API",
    description="A simple API used to test health checks, readiness, observability, and chaos engineering experiments.",
    version="0.2.0",
)


def utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


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

        return {
            "status": "reachable",
            "message": "PostgreSQL connection successful",
        }

    except Exception as error:
        return {
            "status": "unreachable",
            "message": str(error),
        }


def check_redis():
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            socket_connect_timeout=2,
            socket_timeout=2,
        )

        client.ping()

        return {
            "status": "reachable",
            "message": "Redis connection successful",
        }

    except Exception as error:
        return {
            "status": "unreachable",
            "message": str(error),
        }


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
        "timestamp": utc_timestamp(),
    }


@app.get("/ready")
def readiness_check():
    postgres_status = check_postgres()
    redis_status = check_redis()

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
        "version": "0.2.0",
        "environment": os.getenv("APP_ENV", "local"),
        "status": "running",
        "features": {
            "database": postgres_status["status"] == "reachable",
            "cache": redis_status["status"] == "reachable",
            "observability": False,
            "chaos_experiments": False,
        },
        "dependencies": {
            "database": postgres_status,
            "cache": redis_status,
        },
        "timestamp": utc_timestamp(),
    }


@app.get("/simulate-work")
def simulate_work():
    processing_time = round(random.uniform(0.1, 1.5), 2)
    time.sleep(processing_time)

    return {
        "message": "Work simulation completed",
        "processing_time_seconds": processing_time,
        "status": "success",
        "timestamp": utc_timestamp(),
    }