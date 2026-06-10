# Prometheus Alerting Rules — Observability Milestone

![Prometheus](https://img.shields.io/badge/prometheus-alerting%20rules-E6522C.svg)
![Status](https://img.shields.io/badge/status-validated-success.svg)
![Redis](https://img.shields.io/badge/RedisDown-alert%20validated-DC382D.svg)
![PostgreSQL](https://img.shields.io/badge/PostgresDown-alert%20validated-336791.svg)

## Overview

This document records the addition and validation of Prometheus alerting rules for the Chaos Engineering Sandbox API.

The project exposes application and dependency metrics through the FastAPI `/metrics` endpoint. Prometheus alerting rules use those metrics to detect unhealthy conditions automatically.

Validated dependency alerts:

```text
RedisDown
PostgresDown
```

These alerts fire when the related dependency health metric changes from `1` to `0`.

---

## Purpose

The purpose of this milestone is to move the project from basic observability toward operational alerting.

Before this milestone, the system could show metrics in Prometheus and Grafana.

After this milestone, Prometheus can evaluate alert rules and detect when a dependency becomes unhealthy.

This is important because monitoring answers:

```text
What is happening?
```

Alerting answers:

```text
What needs attention?
```

---

## Alert Rules Added

Alert rules are stored in:

```text
observability/prometheus/rules/alerts.yml
```

Prometheus loads this rule file through:

```text
observability/prometheus/prometheus.yml
```

The alert rule folder is mounted into the Prometheus container through Docker Compose.

---

## Configured Alerts

| Alert | Purpose | Severity | Validation Status |
|---|---|---|---|
| `RedisDown` | Fires when Redis dependency health is `0` | warning | Validated |
| `PostgresDown` | Fires when PostgreSQL dependency health is `0` | critical | Validated |
| `ApiHighLatency` | Fires when 95th percentile API latency is above 1 second | warning | Configured |
| `ApiHighErrorRate` | Fires when API returns HTTP 5xx responses | critical | Configured |

---

## Alert Rule File

File:

```text
observability/prometheus/rules/alerts.yml
```

Rules:

```yaml
groups:
  - name: chaos-api-alerts
    rules:
      - alert: RedisDown
        expr: chaos_api_dependency_up{dependency="redis"} == 0
        for: 15s
        labels:
          severity: warning
          service: chaos-api
          dependency: redis
        annotations:
          summary: "Redis dependency is unreachable"
          description: "The Chaos API cannot reach Redis. The redis dependency health metric is 0."

      - alert: PostgresDown
        expr: chaos_api_dependency_up{dependency="postgres"} == 0
        for: 15s
        labels:
          severity: critical
          service: chaos-api
          dependency: postgres
        annotations:
          summary: "PostgreSQL dependency is unreachable"
          description: "The Chaos API cannot reach PostgreSQL. The postgres dependency health metric is 0."

      - alert: ApiHighLatency
        expr: histogram_quantile(0.95, sum(rate(chaos_api_http_request_duration_seconds_bucket[1m])) by (le)) > 1
        for: 30s
        labels:
          severity: warning
          service: chaos-api
        annotations:
          summary: "API latency is high"
          description: "The 95th percentile API latency is above 1 second."

      - alert: ApiHighErrorRate
        expr: sum(rate(chaos_api_http_requests_total{http_status=~"5.."}[1m])) > 0
        for: 30s
        labels:
          severity: critical
          service: chaos-api
        annotations:
          summary: "API 5xx errors detected"
          description: "The Chaos API is returning HTTP 5xx responses."
```

---

## Prometheus Configuration Update

Prometheus was updated to load the alert rule file.

File:

```text
observability/prometheus/prometheus.yml
```

Configuration:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "/etc/prometheus/rules/alerts.yml"

scrape_configs:
  - job_name: "chaos-api"
    metrics_path: "/metrics"
    static_configs:
      - targets:
          - "api:8000"
```

---

## Docker Compose Update

The Prometheus service was updated to mount the alert rules folder.

File:

```text
docker-compose.yml
```

Prometheus volume mount:

```yaml
volumes:
  - ./observability/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
  - ./observability/prometheus/rules:/etc/prometheus/rules:ro
  - prometheus_data:/prometheus
```

This allows Prometheus inside the container to read:

```text
/etc/prometheus/rules/alerts.yml
```

---

## Validation Steps

### 1. Restart Docker Compose

The Docker Compose stack was restarted so Prometheus could load the new rule file.

```bash
docker compose down
docker compose up --build
```

---

### 2. Confirm Rules Loaded in Prometheus

Prometheus was opened in the browser:

```text
http://127.0.0.1:9090
```

The rule page was checked:

```text
Status → Rules
```

The following alert group appeared:

```text
chaos-api-alerts
```

The following alert rules were visible:

```text
RedisDown
PostgresDown
ApiHighLatency
ApiHighErrorRate
```

Initial state:

```text
State: OK
```

This confirmed that Prometheus successfully loaded and evaluated the alert rules.

---

## RedisDown Alert Validation

### 1. Stop Redis

Redis was stopped manually using Docker.

```bash
docker stop chaos-redis
```

### 2. Refresh Dependency Metric

The `/ready` endpoint was called to refresh dependency status.

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
      "status": "unreachable"
    }
  }
}
```

### 3. Confirm Metric Changed

The dependency health metric was checked.

```bash
curl http://127.0.0.1:8000/metrics | grep chaos_api_dependency_up
```

Observed result:

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 0.0
```

This confirmed that Redis was unhealthy while PostgreSQL remained healthy.

### 4. Confirm Alert Fired

The `RedisDown` alert has:

```text
for: 15s
```

After Redis stayed unhealthy for at least 15 seconds, Prometheus showed the `RedisDown` alert firing.

Prometheus alerts page:

```text
http://127.0.0.1:9090/alerts
```

Screenshot evidence:

```text
docs/screenshots/prometheus-redisdown-alert.png
```

### 5. Redis Recovery Validation

Redis was started again.

```bash
docker start chaos-redis
```

The `/ready` endpoint was called again.

```bash
curl http://127.0.0.1:8000/ready
```

The dependency metric returned to healthy state.

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

Prometheus alert state returned to:

```text
OK
```

---

## PostgresDown Alert Validation

### 1. Stop PostgreSQL

PostgreSQL was stopped manually using Docker.

```bash
docker stop chaos-postgres
```

### 2. Refresh Dependency Metric

The `/ready` endpoint was called to refresh dependency status.

```bash
curl http://127.0.0.1:8000/ready
```

Expected result:

```text
status: not_ready
database: unreachable
cache: reachable
```

### 3. Confirm Metric Changed

The dependency health metric was checked.

```bash
curl http://127.0.0.1:8000/metrics | grep chaos_api_dependency_up
```

Expected result:

```text
chaos_api_dependency_up{dependency="postgres"} 0.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

This confirmed that PostgreSQL was unhealthy while Redis remained healthy.

### 4. Confirm Alert Fired

The `PostgresDown` alert has:

```text
for: 15s
```

After PostgreSQL stayed unhealthy for at least 15 seconds, Prometheus showed the `PostgresDown` alert firing.

Prometheus alerts page:

```text
http://127.0.0.1:9090/alerts
```

Screenshot evidence:

```text
docs/screenshots/prometheus-postgresdown-alert.png
```

### 5. PostgreSQL Recovery Validation

PostgreSQL was started again.

```bash
docker start chaos-postgres
```

The `/ready` endpoint was called again.

```bash
curl http://127.0.0.1:8000/ready
```

The dependency metric returned to healthy state.

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

Prometheus alert state returned to:

```text
OK
```

---

## Result Summary

| Check | Result |
|---|---|
| Alert rules file created | Passed |
| Prometheus config updated | Passed |
| Docker Compose rule mount added | Passed |
| Prometheus restarted successfully | Passed |
| Alert group loaded in Prometheus | Passed |
| `RedisDown` rule loaded | Passed |
| `PostgresDown` rule loaded | Passed |
| `ApiHighLatency` rule loaded | Passed |
| `ApiHighErrorRate` rule loaded | Passed |
| Redis failure changed Redis metric to `0` | Passed |
| `RedisDown` alert fired after 15 seconds | Passed |
| Redis recovery changed Redis metric back to `1` | Passed |
| `RedisDown` alert returned to OK | Passed |
| PostgreSQL failure changed PostgreSQL metric to `0` | Passed |
| `PostgresDown` alert fired after 15 seconds | Passed |
| PostgreSQL recovery changed PostgreSQL metric back to `1` | Passed |
| `PostgresDown` alert returned to OK | Passed |
| GitHub Actions passed | Passed |

---

## What This Proves

This milestone proves that the project can detect and alert on dependency failure using Prometheus.

The dependency alerting flow is now:

```text
Dependency fails
 ↓
API /ready detects dependency unreachable
 ↓
chaos_api_dependency_up changes from 1 to 0
 ↓
Prometheus evaluates alert rule
 ↓
Alert fires after configured duration
 ↓
Dependency recovers
 ↓
Metric returns to 1
 ↓
Alert returns to OK
```

This has been validated for both Redis and PostgreSQL.

---

## Why This Matters

In real operations, engineers should not need to manually refresh endpoints to know when a system is unhealthy.

Alerting rules help detect problems automatically.

This milestone demonstrates:

- Metrics-based alerting.
- Dependency-specific alert detection.
- Alert recovery.
- Prometheus rule configuration.
- Docker Compose observability configuration.
- Practical DevOps/SRE troubleshooting workflow.

---

## Current Alerting Limitations

This setup currently validates alert evaluation inside Prometheus only.

Limitations:

- No Alertmanager integration yet.
- No email, Slack, or webhook notifications yet.
- `ApiHighLatency` is configured but not yet separately validated.
- `ApiHighErrorRate` is configured but not yet separately validated.
- Alert screenshots are currently manual.

These are acceptable for the current milestone because the main goal was to load rules and validate real firing alerts for dependency failure.

---

## Future Improvements

Recommended next improvements:

- Validate `ApiHighLatency` alert.
- Validate `ApiHighErrorRate` alert.
- Add Alertmanager.
- Add notification routing.
- Add email or webhook receiver.
- Add Grafana alerting comparison.
- Add alert recovery screenshots.
- Add incident report for alerting validation.
- Add documentation for alert severity levels.
- Add dashboard panel showing active alerts.
- Add automated alert tests.

---

## Final Result

Prometheus alerting rules were successfully added and dependency alerts were validated.

```text
Final result: PASS
Rules loaded: Yes
RedisDown alert validated: Yes
PostgresDown alert validated: Yes
Redis recovery validated: Yes
PostgreSQL recovery validated: Yes
Alerts returned to OK: Yes
GitHub Actions passed: Yes
```
