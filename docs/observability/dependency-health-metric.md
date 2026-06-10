# Dependency Health Metric — Observability Milestone

![Prometheus](https://img.shields.io/badge/prometheus-dependency%20metric-E6522C.svg)
![Grafana](https://img.shields.io/badge/grafana-dependency%20health%20panel-F46800.svg)
![Status](https://img.shields.io/badge/status-validated-success.svg)
![Redis](https://img.shields.io/badge/redis-failure%20metric%20validated-DC382D.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-health%20metric-336791.svg)

## Overview

This document records the addition and validation of a dependency health metric for the Chaos Engineering Sandbox API.

The metric allows Prometheus and Grafana to show whether the API's external dependencies are reachable.

Current dependencies:

- PostgreSQL
- Redis

The metric is exposed through the FastAPI `/metrics` endpoint and visualised in Grafana.

---

## Metric Name

```text
chaos_api_dependency_up
```

## Metric Type

```text
Gauge
```

## Metric Labels

| Label | Purpose |
|---|---|
| `dependency` | Identifies which dependency is being checked |

Current label values:

```text
postgres
redis
```

## Metric Meaning

| Value | Meaning |
|---|---|
| `1` | Dependency is reachable |
| `0` | Dependency is unreachable |

Example healthy state:

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

Example Redis failure state:

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 0.0
```

---

## Why This Metric Was Added

Before this metric, the API could already report dependency readiness through the `/ready` endpoint.

However, Prometheus and Grafana needed a direct numerical metric that could be queried, graphed, visualised, and later used for alerting.

The dependency health metric solves this by converting dependency status into a simple numerical value.

```text
reachable   → 1
unreachable → 0
```

---

## Code Change Summary

A new Prometheus Gauge was added to the API.

```python
DEPENDENCY_UP = Gauge(
    "chaos_api_dependency_up",
    "Dependency health status where 1 means reachable and 0 means unreachable",
    ["dependency"],
)
```

The `/ready` endpoint now updates the metric after checking PostgreSQL and Redis.

```python
DEPENDENCY_UP.labels(dependency="postgres").set(
    1 if postgres_status["status"] == "reachable" else 0
)

DEPENDENCY_UP.labels(dependency="redis").set(
    1 if redis_status["status"] == "reachable" else 0
)
```

This means every `/ready` check also refreshes the dependency health metric.

---

## Validation Steps

### 1. Confirm Tests Passed

The test suite was run locally.

```bash
pytest
```

Result:

```text
6 passed
```

Warnings were shown from dependency libraries, but there were no test failures.

---

### 2. Start Docker Compose Stack

The Docker Compose stack was rebuilt and started.

```bash
docker compose up --build
```

The stack includes:

```text
chaos-api
chaos-postgres
chaos-redis
chaos-prometheus
chaos-grafana
```

---

### 3. Call `/ready`

The `/ready` endpoint was called to refresh dependency status.

```bash
curl http://127.0.0.1:8000/ready
```

Healthy result:

```json
{
  "status": "ready",
  "service": "chaos-api",
  "dependencies": {
    "database": {
      "status": "reachable",
      "message": "PostgreSQL connection successful"
    },
    "cache": {
      "status": "reachable",
      "message": "Redis connection successful"
    }
  }
}
```

---

### 4. Confirm Metric Appears in `/metrics`

The `/metrics` endpoint was checked.

```bash
curl http://127.0.0.1:8000/metrics | grep chaos_api_dependency_up
```

Healthy result:

```text
# HELP chaos_api_dependency_up Dependency health status where 1 means reachable and 0 means unreachable
# TYPE chaos_api_dependency_up gauge
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

This confirmed that both PostgreSQL and Redis were reachable.

---

## Redis Failure Validation

Redis was stopped manually using Docker.

```bash
docker stop chaos-redis
```

The `/ready` endpoint was called again.

```bash
curl http://127.0.0.1:8000/ready
```

Observed result:

```json
{
  "status": "not_ready",
  "service": "chaos-api",
  "dependencies": {
    "database": {
      "status": "reachable",
      "message": "PostgreSQL connection successful"
    },
    "cache": {
      "status": "unreachable",
      "message": "Error -2 connecting to redis:6379. Name or service not known."
    }
  }
}
```

The dependency health metric was checked again.

```bash
curl http://127.0.0.1:8000/metrics | grep chaos_api_dependency_up
```

Failure result:

```text
# HELP chaos_api_dependency_up Dependency health status where 1 means reachable and 0 means unreachable
# TYPE chaos_api_dependency_up gauge
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 0.0
```

This confirmed that:

```text
PostgreSQL remained healthy.
Redis became unhealthy.
The metric changed Redis from 1 to 0.
```

---

## Redis Recovery Validation

Redis was started again.

```bash
docker start chaos-redis
```

The `/ready` endpoint was called again.

```bash
curl http://127.0.0.1:8000/ready
```

Observed result:

```json
{
  "status": "ready",
  "service": "chaos-api",
  "dependencies": {
    "database": {
      "status": "reachable",
      "message": "PostgreSQL connection successful"
    },
    "cache": {
      "status": "reachable",
      "message": "Redis connection successful"
    }
  }
}
```

The metric returned to healthy state.

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

This confirmed that the metric updated correctly after Redis recovered.

---

## Grafana Dashboard Update

The Grafana dashboard was updated with a new panel.

Panel name:

```text
Dependency Health
```

Prometheus query:

```promql
avg by (dependency) (chaos_api_dependency_up)
```

Panel purpose:

```text
Shows PostgreSQL and Redis dependency health. 1 means reachable and 0 means unreachable.
```

The updated dashboard JSON was exported and saved to:

```text
observability/grafana/dashboards/chaos-api-observability-dashboard.json
```

Screenshot evidence was saved to:

```text
docs/screenshots/dependency-health-panel.png
```

---

## Result Summary

| Check | Result |
|---|---|
| Dependency metric added to API | Passed |
| Metric exposed through `/metrics` | Passed |
| PostgreSQL healthy state shows `1.0` | Passed |
| Redis healthy state shows `1.0` | Passed |
| Redis failure changes Redis metric to `0.0` | Passed |
| PostgreSQL remains `1.0` during Redis failure | Passed |
| Redis recovery changes Redis metric back to `1.0` | Passed |
| Grafana Dependency Health panel added | Passed |
| Dashboard JSON exported | Passed |
| GitHub Actions passed | Passed |

---

## What This Proves

This milestone proves that the system can expose dependency health as machine-readable metrics.

The system can now show:

```text
API process health
API readiness
Request count
Request rate
Request latency
In-progress requests
PostgreSQL dependency health
Redis dependency health
```

This is a stronger observability setup than relying only on logs or manual `/ready` checks.

---

## Why This Matters

In real operations, teams need to know not only that a service is unhealthy, but also why it is unhealthy.

Without dependency metrics, an operator may only see that the API is not ready.

With dependency metrics, the operator can see which dependency is causing the problem.

Example:

```text
API readiness: not_ready
PostgreSQL: 1
Redis: 0
```

This makes troubleshooting faster and clearer.

---

## Future Improvements

Recommended next improvements:

- Add Prometheus alert rule for Redis dependency failure.
- Add Prometheus alert rule for PostgreSQL dependency failure.
- Add Grafana alerting for dependency health.
- Add dependency health screenshot to README.
- Add PostgreSQL failure validation for the dependency metric.
- Add dependency status history panels.
- Add MTTR measurement for dependency recovery.
- Add alert documentation.

---

## Final Result

The dependency health metric was successfully added, validated, visualised, exported, and committed.

```text
Final result: PASS
Metric added: Yes
Redis failure detected by metric: Yes
Redis recovery detected by metric: Yes
Grafana panel added: Yes
GitHub Actions passed: Yes
```
