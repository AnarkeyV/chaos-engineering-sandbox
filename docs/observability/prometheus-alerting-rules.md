# Prometheus Alerting Rules — Observability Milestone

![Prometheus](https://img.shields.io/badge/prometheus-alerting%20rules-E6522C.svg)
![Status](https://img.shields.io/badge/status-fully%20validated-success.svg)
![Redis](https://img.shields.io/badge/RedisDown-validated-DC382D.svg)
![PostgreSQL](https://img.shields.io/badge/PostgresDown-validated-336791.svg)
![Latency](https://img.shields.io/badge/ApiHighLatency-validated-orange.svg)
![Errors](https://img.shields.io/badge/ApiHighErrorRate-validated-red.svg)

## Overview

This document records the addition and validation of Prometheus alerting rules for the Chaos Engineering Sandbox API.

The project exposes application and dependency metrics through the FastAPI `/metrics` endpoint. Prometheus alerting rules use those metrics to detect unhealthy conditions automatically.

Validated alerts:

```text
RedisDown
PostgresDown
ApiHighLatency
ApiHighErrorRate
```

These alerts prove that the system can detect dependency failures, high latency, and HTTP 5xx errors.

---

## Purpose

The purpose of this milestone is to move the project from basic observability toward operational alerting.

Before this milestone, the system could show metrics in Prometheus and Grafana.

After this milestone, Prometheus can evaluate alert rules and detect when the system requires attention.

This is important because monitoring answers:

```text
What is happening?
```

Alerting answers:

```text
What needs attention?
```

---

## Alert Rules Location

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

## Configured and Validated Alerts

| Alert | Purpose | Severity | Validation Status |
|---|---|---|---|
| `RedisDown` | Fires when Redis dependency health is `0` | warning | Validated |
| `PostgresDown` | Fires when PostgreSQL dependency health is `0` | critical | Validated |
| `ApiHighLatency` | Fires when 95th percentile API latency is above 1 second | warning | Validated |
| `ApiHighErrorRate` | Fires when API returns HTTP 5xx responses | critical | Validated |

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

## Prometheus Configuration

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

## Docker Compose Configuration

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

## Supporting Test Endpoints

Two controlled test endpoints were added to support alert validation.

### `/simulate-work`

The `/simulate-work` endpoint supports a delay parameter.

Example:

```bash
curl "http://127.0.0.1:8000/simulate-work?delay=2"
```

Purpose:

```text
Generate slow API responses to validate ApiHighLatency.
```

### `/simulate-error`

The `/simulate-error` endpoint intentionally returns HTTP 500.

Example:

```bash
curl http://127.0.0.1:8000/simulate-error
```

Purpose:

```text
Generate HTTP 500 responses to validate ApiHighErrorRate.
```

---

## Rule Loading Validation

The Docker Compose stack was restarted so Prometheus could load the new rule file.

```bash
docker compose down
docker compose up --build
```

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

This confirmed that Prometheus successfully loaded and evaluated the alert rules.

---

## RedisDown Alert Validation

Redis was stopped manually using Docker.

```bash
docker stop chaos-redis
```

The `/ready` endpoint was called to refresh dependency status.

```bash
curl http://127.0.0.1:8000/ready
```

Observed dependency metric:

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 0.0
```

After Redis stayed unhealthy for at least 15 seconds, Prometheus showed the `RedisDown` alert firing.

Screenshot evidence:

```text
docs/screenshots/prometheus-redisdown-alert.png
```

Redis was then restarted:

```bash
docker start chaos-redis
```

The metric returned to:

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

The alert returned to OK.

---

## PostgresDown Alert Validation

PostgreSQL was stopped manually using Docker.

```bash
docker stop chaos-postgres
```

The `/ready` endpoint was called to refresh dependency status.

```bash
curl http://127.0.0.1:8000/ready
```

Observed dependency metric:

```text
chaos_api_dependency_up{dependency="postgres"} 0.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

After PostgreSQL stayed unhealthy for at least 15 seconds, Prometheus showed the `PostgresDown` alert firing.

Screenshot evidence:

```text
docs/screenshots/prometheus-postgresdown-alert.png
```

PostgreSQL was then restarted:

```bash
docker start chaos-postgres
```

The metric returned to:

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

The alert returned to OK.

---

## ApiHighLatency Alert Validation

The `/simulate-work` endpoint was updated to support a delay parameter.

Example:

```bash
curl "http://127.0.0.1:8000/simulate-work?delay=2"
```

Slow requests were generated:

```bash
for i in {1..25}; do
  echo "Slow request $i"
  curl -s "http://127.0.0.1:8000/simulate-work?delay=2" > /dev/null
done
```

This increased the 95th percentile API latency above the configured alert threshold.

Alert rule:

```promql
histogram_quantile(0.95, sum(rate(chaos_api_http_request_duration_seconds_bucket[1m])) by (le)) > 1
```

After the high latency condition persisted for the configured duration, Prometheus showed the `ApiHighLatency` alert firing.

Screenshot evidence:

```text
docs/screenshots/prometheus-apihighlatency-alert.png
```

---

## ApiHighErrorRate Alert Validation

A controlled error endpoint was added:

```text
/simulate-error
```

This endpoint intentionally returns HTTP 500 for alert validation.

500 errors were generated:

```bash
for i in {1..20}; do
  echo "Error request $i"
  curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/simulate-error
  sleep 1
done
```

Expected response:

```text
500
```

The API metrics showed HTTP 500 responses.

Example metric:

```text
chaos_api_http_requests_total{endpoint="/simulate-error",http_status="500",method="GET"} 20.0
```

Alert rule:

```promql
sum(rate(chaos_api_http_requests_total{http_status=~"5.."}[1m])) > 0
```

After the error condition persisted for the configured duration, Prometheus showed the `ApiHighErrorRate` alert firing.

Screenshot evidence:

```text
docs/screenshots/prometheus-apihigherrorrate-alert.png
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
| `RedisDown` alert validated | Passed |
| `PostgresDown` alert validated | Passed |
| `ApiHighLatency` alert validated | Passed |
| `ApiHighErrorRate` alert validated | Passed |
| Redis alert returned to OK after recovery | Passed |
| PostgreSQL alert returned to OK after recovery | Passed |
| `/simulate-work?delay=2` added | Passed |
| `/simulate-error` added | Passed |
| Tests updated and passed | Passed |
| GitHub Actions passed | Passed |

---

## What This Proves

This milestone proves that the project can detect and alert on dependency failure, high latency, and API error responses using Prometheus.

The alerting flow is now:

```text
Failure or degraded behavior occurs
 ↓
API exposes metric
 ↓
Prometheus scrapes metric
 ↓
Prometheus evaluates alert rule
 ↓
Alert fires after configured duration
 ↓
Issue is recovered
 ↓
Metric returns to healthy state
 ↓
Alert returns to OK
```

Validated alert categories:

```text
Dependency failure
High latency
HTTP 5xx error rate
```

---

## Why This Matters

In real operations, engineers should not need to manually refresh endpoints to know when a system is unhealthy.

Alerting rules help detect problems automatically.

This milestone demonstrates:

- Metrics-based alerting.
- Dependency-specific alert detection.
- Application latency alerting.
- HTTP 5xx error alerting.
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
- Alert screenshots are currently manual.
- The test endpoints are intentionally simple and used only for local validation.
- The project does not yet include automated alert tests.

These are acceptable for this milestone because the goal was to load and validate real Prometheus alert rules locally.

---

## Future Improvements

Recommended next improvements:

- Add Alertmanager.
- Add notification routing.
- Add email or webhook receiver.
- Add Grafana alerting comparison.
- Add dashboard panel showing active alerts.
- Add automated alert tests.
- Add alert severity documentation.
- Add MTTR measurement for alert recovery.
- Add cloud alerting comparison for Azure Monitor or managed Prometheus.

---

## Final Result

Prometheus alerting rules were successfully added and all configured alerts were validated.

```text
Final result: PASS
Rules loaded: Yes
RedisDown alert validated: Yes
PostgresDown alert validated: Yes
ApiHighLatency alert validated: Yes
ApiHighErrorRate alert validated: Yes
Alerts returned to OK where applicable: Yes
GitHub Actions passed: Yes
```
