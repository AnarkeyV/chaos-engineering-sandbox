# Chaos Engineering Sandbox — Project Roadmap

## Project Purpose

The Chaos Engineering Sandbox is a hands-on DevOps, Cloud Support, Kubernetes, observability, and resilience engineering portfolio project.

The project is designed to show the full reliability workflow:

```text
Build
Test
Deploy
Break
Detect
Recover
Improve
Validate
Observe
Automate
Document
```

The goal is not only to prove that an application works, but to show how it behaves when things fail.

---

## Current Roadmap Status

| Milestone | Status |
|---|---|
| Milestone 1 — Project setup and repository structure | Completed |
| Milestone 2 — FastAPI backend and automated tests | Completed |
| Milestone 3 — Docker and Docker Compose multi-service setup | Completed |
| Milestone 4 — Kubernetes local deployment with Kind | Completed |
| Milestone 5 — Observability with Prometheus and Grafana | Completed |
| Milestone 6 — Dependency failure testing | Completed |
| Milestone 7 — Screenshot evidence and README polish | Completed |
| Milestone 8 — Dependency health metrics and alerting | Completed |
| Milestone 9 — Automated chaos experiments | Planned |
| Milestone 10 — Cloud deployment extension | Planned |
| Milestone 11 — Final case study report | Planned |

---

## Milestone 1 — Project Setup and Repository Structure

### Status

Completed

### Objective

Create the initial project repository and organise it using a clear DevOps portfolio structure.

### Completed Work

- Created public GitHub repository.
- Created project folder structure.
- Added root `README.md`.
- Added `.gitignore`.
- Added MIT `LICENSE`.
- Added documentation folder.
- Added roadmap file.
- Added architecture notes.
- Pushed initial project structure to GitHub.

### Key Files

```text
README.md
LICENSE
.gitignore
docs/project-roadmap.md
docs/architecture-notes.md
```

---

## Milestone 2 — FastAPI Backend and Automated Tests

### Status

Completed

### Objective

Build a small API service that can be used for health checks, readiness checks, failure testing, and observability.

### Completed Work

- Created FastAPI backend.
- Added root endpoint.
- Added `/health` endpoint.
- Added `/ready` endpoint.
- Added `/status` endpoint.
- Added `/simulate-work` endpoint.
- Added `/metrics` endpoint later during observability milestone.
- Added pytest tests.
- Added GitHub Actions CI workflow.
- Fixed Python import issues using package files and `pytest.ini`.
- Confirmed GitHub Actions passed.

### Key Files

```text
app/api/main.py
app/api/requirements.txt
tests/test_api.py
pytest.ini
.github/workflows/ci.yml
```

### Completed Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Root API response |
| `/health` | Confirms API process is alive |
| `/ready` | Checks dependency readiness |
| `/status` | Shows service status and feature information |
| `/simulate-work` | Simulates API work |
| `/metrics` | Exposes Prometheus metrics |

---

## Milestone 3 — Docker and Docker Compose Multi-Service Setup

### Status

Completed

### Objective

Containerise the API and run it locally with PostgreSQL and Redis dependencies.

### Completed Work

- Created API Dockerfile.
- Created `.dockerignore`.
- Added Docker build validation to GitHub Actions.
- Created Docker Compose setup.
- Added PostgreSQL service.
- Added Redis service.
- Added Docker Compose health checks.
- Added dependency-aware API readiness checks.
- Confirmed API can detect PostgreSQL and Redis dependency state.
- Completed manual Redis failure test in Docker Compose.

### Key Files

```text
app/api/Dockerfile
.dockerignore
docker-compose.yml
docs/incident-reports/01-redis-manual-failure-test.md
```

### Outcome

The API can run as part of a multi-service local stack and report whether PostgreSQL and Redis are reachable.

---

## Milestone 4 — Kubernetes Local Deployment with Kind

### Status

Completed

### Objective

Deploy the API, PostgreSQL, and Redis into a local Kubernetes cluster using Kind.

### Completed Work

- Created local Kind cluster.
- Created Kubernetes namespace.
- Created API Deployment and Service.
- Created PostgreSQL Deployment and Service.
- Created Redis Deployment and Service.
- Added liveness probes.
- Added readiness probes.
- Loaded API Docker image into Kind.
- Confirmed pods reached `Running` and `Ready`.
- Confirmed API can be accessed using `kubectl port-forward`.
- Completed Kubernetes API pod failure test.
- Improved API Deployment from one replica to two replicas.
- Completed two-replica availability test.

### Key Files

```text
k8s/namespace.yaml
k8s/api-deployment.yaml
k8s/api-service.yaml
k8s/postgres-deployment.yaml
k8s/postgres-service.yaml
k8s/redis-deployment.yaml
k8s/redis-service.yaml
docs/kubernetes-local-deployment.md
docs/incident-reports/02-kubernetes-api-pod-failure-test.md
docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md
docs/incident-reports/04-two-replica-api-availability-test.md
```

### Outcome

The API runs locally in Kubernetes with two replicas and can survive deletion of one API pod while maintaining availability.

---

## Milestone 5 — Observability with Prometheus and Grafana

### Status

Completed

### Objective

Add observability to the project so API behavior can be monitored visually and through metrics.

### Completed Work

- Added Prometheus client library.
- Added `/metrics` endpoint to FastAPI.
- Added custom API metrics.
- Added Prometheus service to Docker Compose.
- Added Prometheus scrape configuration.
- Confirmed Prometheus can scrape API metrics.
- Added Grafana service to Docker Compose.
- Provisioned Prometheus datasource in Grafana.
- Created Grafana dashboard.
- Exported dashboard JSON.
- Generated traffic to validate dashboard panels.
- Added screenshot evidence to README.

### Key Files

```text
observability/prometheus/prometheus.yml
observability/grafana/provisioning/datasources/prometheus.yml
observability/grafana/dashboards/chaos-api-observability-dashboard.json
docs/screenshots/grafana-dashboard.png
docs/screenshots/prometheus-query.png
```

### Custom Metrics

| Metric | Purpose |
|---|---|
| `chaos_api_http_requests_total` | Counts API requests by method, endpoint, and status code |
| `chaos_api_http_request_duration_seconds` | Tracks request latency |
| `chaos_api_http_requests_in_progress` | Tracks active requests |

### Grafana Dashboard Panels

| Panel | Purpose |
|---|---|
| Total API Requests | Shows total request count |
| API Request Rate | Shows requests per second |
| Requests by Endpoint | Shows endpoint traffic |
| Request Rate by Endpoint | Shows endpoint request rate |
| 95th Percentile Request Latency | Shows latency behavior |
| In-Progress Requests | Shows active requests |

### Outcome

The system now has a working observability stack using Prometheus and Grafana.

---

## Milestone 6 — Dependency Failure Testing

### Status

Completed

### Objective

Test how the Kubernetes system behaves when dependency pods fail.

### Completed Work

- Completed Kubernetes Redis failure test.
- Completed Kubernetes PostgreSQL failure test.
- Documented different recovery behavior between Redis and PostgreSQL.
- Confirmed Kubernetes recreated dependency pods.
- Confirmed API readiness detects PostgreSQL failure.
- Confirmed Redis remained reachable during PostgreSQL failure.
- Added incident reports for both dependency failure tests.

### Redis Failure Test

Redis pod was manually deleted.

Result:

| Check | Result |
|---|---|
| Redis pod deleted | Yes |
| Kubernetes recreated Redis pod | Yes |
| Redis Deployment returned to `1/1` | Yes |
| API stayed running | Yes |
| Visible `/ready` interruption captured | No |

Key observation:

```text
No visible readiness interruption was captured during the 1-second polling loop.
```

Incident report:

```text
docs/incident-reports/05-kubernetes-redis-failure-test.md
```

### PostgreSQL Failure Test

PostgreSQL pod was manually deleted.

Result:

| Check | Result |
|---|---|
| PostgreSQL pod deleted | Yes |
| API stayed running | Yes |
| Redis stayed reachable | Yes |
| Database became unreachable | Yes |
| `/ready` became `not_ready` | Yes |
| Kubernetes recreated PostgreSQL pod | Yes |
| PostgreSQL Deployment returned to `1/1` | Yes |
| API `/ready` returned to `ready` | Yes |

Observed readiness impact:

```text
Request 17–24: not_ready
Request 25: ready
```

Incident report:

```text
docs/incident-reports/06-kubernetes-postgresql-failure-test.md
```

### Dependency Failure Comparison

| Dependency | Failure Result |
|---|---|
| Redis | No visible readiness interruption captured |
| PostgreSQL | Clear `not_ready` state observed |
| Redis recovery | Very fast during observed test |
| PostgreSQL recovery | Visible readiness impact |
| API process | Stayed running in both tests |

### Outcome

The project now demonstrates dependency-aware readiness behavior and Kubernetes recovery for both cache and database components.

---

## Milestone 7 — Screenshot Evidence and README Polish

### Status

Completed

### Objective

Make the project easier to review visually by adding screenshots and updating the README.

### Completed Work

- Added Grafana dashboard screenshot.
- Added Prometheus query screenshot.
- Added PostgreSQL failure readiness screenshot.
- Added Screenshots / Evidence section to README.
- Confirmed images display properly on GitHub.
- Confirmed GitHub Actions passed after README and screenshot update.

### Key Files

```text
docs/screenshots/grafana-dashboard.png
docs/screenshots/prometheus-query.png
docs/screenshots/postgresql-failure-readiness.png
README.md
```

### Outcome

The README now includes visual proof of monitoring and failure testing results, making the repository more portfolio-friendly.

---

## Current Incident Reports

| Report | Status | Description |
|---|---|---|
| `01-redis-manual-failure-test.md` | Completed | Redis failure in Docker Compose |
| `02-kubernetes-api-pod-failure-test.md` | Completed | API pod deletion and Kubernetes recovery |
| `03-kubernetes-api-replica-resilience-improvement.md` | Completed | API scaled from one replica to two |
| `04-two-replica-api-availability-test.md` | Completed | 60/60 successful requests during API pod failure |
| `05-kubernetes-redis-failure-test.md` | Completed | Redis pod deletion and Kubernetes recovery |
| `06-kubernetes-postgresql-failure-test.md` | Completed | PostgreSQL failure detection and recovery |

---

## Milestone 8 — Dependency Health Metrics and Alerting

### Status

In progress — Part 1 completed

### Objective

Move the project from basic observability toward reliability-focused metrics and alerting.

The first part of this milestone adds a direct dependency health metric so Prometheus and Grafana can show whether PostgreSQL and Redis are reachable.

---

### Part 1 — Dependency Health Metric

#### Status

Completed

#### Completed Work

- Added new Prometheus Gauge metric.
- Updated `/ready` so dependency checks refresh the metric.
- Validated healthy metric state.
- Stopped Redis manually to validate unhealthy metric state.
- Restarted Redis and confirmed metric recovery.
- Added Grafana Dependency Health panel.
- Exported updated Grafana dashboard JSON.
- Added screenshot evidence.
- Added observability documentation.
- Confirmed GitHub Actions passed.

#### Metric Name

```text
chaos_api_dependency_up
```

#### Metric Meaning

| Value | Meaning |
|---|---|
| `1` | Dependency is reachable |
| `0` | Dependency is unreachable |

#### Healthy State

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

#### Redis Failure State

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 0.0
```

#### Redis Recovery State

```text
chaos_api_dependency_up{dependency="postgres"} 1.0
chaos_api_dependency_up{dependency="redis"} 1.0
```

#### Grafana Panel

Panel name:

```text
Dependency Health
```

Prometheus query:

```promql
avg by (dependency) (chaos_api_dependency_up)
```

#### Key Files

```text
app/api/main.py
observability/grafana/dashboards/chaos-api-observability-dashboard.json
docs/observability/dependency-health-metric.md
docs/screenshots/dependency-health-panel.png
```

#### Outcome

The system can now show which dependency is unhealthy through Prometheus and Grafana.

This improves troubleshooting because the operator can distinguish between:

```text
API process is down
API is alive but not ready
PostgreSQL is unreachable
Redis is unreachable
```

---

### Part 2 — Prometheus Alerting Rules

#### Status

Completed

#### Completed Work

- Created Prometheus alert rules folder.
- Added `alerts.yml`.
- Updated Prometheus configuration to load rule files.
- Updated Docker Compose to mount alert rules into Prometheus.
- Restarted Docker Compose stack.
- Confirmed alert rules loaded in Prometheus.
- Validated `RedisDown` alert by stopping Redis.
- Confirmed Redis dependency metric changed from `1.0` to `0.0`.
- Confirmed `RedisDown` fired after 15 seconds.
- Restarted Redis.
- Confirmed alert returned to OK after recovery.
- Added screenshot evidence.
- Added alerting documentation.
- Confirmed GitHub Actions passed.

#### Configured Alerts

| Alert | Purpose | Severity |
|---|---|---|
| `RedisDown` | Fires when Redis dependency health is `0` | warning |
| `PostgresDown` | Fires when PostgreSQL dependency health is `0` | critical |
| `ApiHighLatency` | Fires when 95th percentile API latency is above 1 second | warning |
| `ApiHighErrorRate` | Fires when API returns HTTP 5xx responses | critical |

#### Validated Alert

```text
RedisDown
```

Validation result:

```text
Redis stopped
 ↓
chaos_api_dependency_up{dependency="redis"} changed to 0.0
 ↓
RedisDown fired after 15 seconds
 ↓
Redis restarted
 ↓
chaos_api_dependency_up{dependency="redis"} returned to 1.0
 ↓
RedisDown returned to OK
```

#### Key Files

```text
observability/prometheus/prometheus.yml
observability/prometheus/rules/alerts.yml
docker-compose.yml
docs/observability/prometheus-alerting-rules.md
docs/screenshots/prometheus-redisdown-alert.png
```

#### Outcome

Prometheus can now evaluate alert rules and detect dependency failure automatically.

This moves the project from passive monitoring toward active alerting.


---

### Part 3 — Reliability Metrics

#### Status

Planned

#### Planned Work

- Add readiness status metric.
- Add dependency check duration metric.
- Add MTTR measurement notes.
- Add dashboard panels for dependency history.
- Add dashboard panels for readiness failure count.

#### Possible Future Metrics

| Metric | Purpose |
|---|---|
| `chaos_api_readiness_status` | Shows whether the API is ready |
| `chaos_api_dependency_check_duration_seconds` | Measures dependency check latency |
| `chaos_api_dependency_failures_total` | Counts dependency failures |

### Part 3 — PostgresDown Alert Validation

#### Status

Completed

#### Completed Work

- Stopped PostgreSQL manually using Docker.
- Called `/ready` to refresh dependency health.
- Confirmed PostgreSQL metric changed from `1.0` to `0.0`.
- Confirmed Redis stayed healthy at `1.0`.
- Waited for the configured alert duration.
- Confirmed `PostgresDown` fired in Prometheus.
- Started PostgreSQL again.
- Confirmed PostgreSQL metric returned to `1.0`.
- Confirmed `PostgresDown` returned to OK.
- Added screenshot evidence.
- Confirmed GitHub Actions passed.

#### Validated Alert

```text
PostgresDown
```

Validation result:

```text
PostgreSQL stopped
 ↓
chaos_api_dependency_up{dependency="postgres"} changed to 0.0
 ↓
chaos_api_dependency_up{dependency="redis"} remained 1.0
 ↓
PostgresDown fired after 15 seconds
 ↓
PostgreSQL restarted
 ↓
chaos_api_dependency_up{dependency="postgres"} returned to 1.0
 ↓
PostgresDown returned to OK
```

#### Key Files

```text
docs/screenshots/prometheus-postgresdown-alert.png
docs/observability/prometheus-alerting-rules.md
```

#### Outcome

Both core dependency alerts are now validated:

```text
RedisDown
PostgresDown
```

This confirms that Prometheus can alert on both cache and database dependency failures.

---

### Part 4 — ApiHighLatency Alert Validation

#### Status

Completed

#### Completed Work

- Updated `/simulate-work` to support a delay parameter.
- Preserved backward-compatible response fields for existing tests.
- Ran pytest successfully.
- Rebuilt Docker Compose stack.
- Generated slow requests using `/simulate-work?delay=2`.
- Confirmed `ApiHighLatency` fired in Prometheus.
- Added screenshot evidence.
- Confirmed GitHub Actions passed.

#### Validated Alert

```text
ApiHighLatency
```

Validation result:

```text
Slow API requests generated
 ↓
95th percentile latency increased
 ↓
ApiHighLatency fired
```

#### Key Files

```text
app/api/main.py
docs/screenshots/prometheus-apihighlatency-alert.png
```

---

### Part 5 — ApiHighErrorRate Alert Validation

#### Status

Completed

#### Completed Work

- Added `/simulate-error` endpoint.
- Added pytest test for `/simulate-error`.
- Ran pytest successfully with 7 passing tests.
- Rebuilt Docker Compose stack.
- Generated HTTP 500 responses.
- Confirmed 500 responses appeared in Prometheus metrics.
- Confirmed `ApiHighErrorRate` fired in Prometheus.
- Added screenshot evidence.
- Confirmed GitHub Actions passed.

#### Validated Alert

```text
ApiHighErrorRate
```

Validation result:

```text
HTTP 500 responses generated
 ↓
chaos_api_http_requests_total{http_status="500"} increased
 ↓
ApiHighErrorRate fired
```

#### Key Files

```text
app/api/main.py
tests/test_api.py
docs/screenshots/prometheus-apihigherrorrate-alert.png
```

---

### Part 6 — Final Milestone 8 Documentation Polish

#### Status

Completed

#### Completed Work

- Updated Prometheus alerting documentation.
- Updated README.
- Updated project roadmap.
- Confirmed all alert validation screenshots are referenced.
- Confirmed GitHub Actions passed.

#### Outcome

Milestone 8 is complete.

The project now includes:

```text
Dependency health metrics
Grafana Dependency Health panel
Prometheus alert rules
RedisDown validation
PostgresDown validation
ApiHighLatency validation
ApiHighErrorRate validation
Screenshot evidence
Documentation updates
```

---

### Overall Milestone 8 Outcome So Far

Milestone 8 is complete.

The project now has dependency-specific health metrics, a Grafana Dependency Health panel, and Prometheus alerting rules validated for RedisDown, PostgresDown, ApiHighLatency, and ApiHighErrorRate.


---

## Milestone 9 — Automated Chaos Experiments

### Status

Planned

### Objective

Move from manual failure testing to repeatable automated chaos experiments.

### Planned Work

- Research LitmusChaos or Chaos Mesh.
- Add basic pod delete chaos experiment.
- Add Redis pod failure experiment.
- Add PostgreSQL pod failure experiment.
- Add experiment documentation.
- Compare manual testing with automated chaos testing.

### Expected Outcome

Failure testing becomes repeatable, documented, and closer to real chaos engineering practice.

---

## Milestone 10 — Cloud Deployment Extension

### Status

Planned

### Objective

Extend the project beyond local development and prepare it for a cloud-based Kubernetes environment.

### Planned Work

- Prepare Azure AKS deployment notes.
- Add cloud architecture diagram.
- Add Terraform planning section.
- Add cost-control notes.
- Add cloud security notes.
- Add managed database comparison.
- Add cloud monitoring comparison.

### Expected Outcome

The project can be explained as both a local learning sandbox and a possible cloud deployment architecture.

---

## Milestone 11 — Final Case Study Report

### Status

Planned

### Objective

Create a final case study that explains the project from a DevOps, Cloud Support, and SRE perspective.

### Planned Work

- Summarise architecture.
- Summarise failure tests.
- Summarise observability setup.
- Summarise key lessons learned.
- Add screenshots.
- Add incident timeline.
- Add final technical reflection.
- Create a PDF case study version.

### Expected Outcome

The project can be presented clearly in interviews, LinkedIn posts, portfolio websites, and job applications.

---

## Current Completed Skills Map

| Skill Area | Evidence |
|---|---|
| Git and GitHub | Public repository, commits, README updates |
| Python API Development | FastAPI service |
| Automated Testing | pytest |
| CI/CD | GitHub Actions |
| Docker | Dockerfile and image build |
| Docker Compose | API, PostgreSQL, Redis, Prometheus, Grafana |
| Kubernetes | Kind, Deployments, Services, probes |
| Reliability Testing | API pod failure, Redis failure, PostgreSQL failure |
| Availability Testing | 60/60 successful request test |
| Observability | Prometheus metrics, dependency health metric, Grafana dashboard, and Prometheus alerting rules |
| Alerting | Prometheus RedisDown, PostgresDown, ApiHighLatency, and ApiHighErrorRate validation |
| Incident Documentation | Six incident reports |
| Scripting | Reusable Bash availability test script |
| Portfolio Communication | README, screenshots, roadmap, reports |

---

## Current Project Summary

The project has moved from a basic API into a complete local reliability engineering sandbox.

Current capabilities:

```text
FastAPI application
Docker containerisation
Docker Compose multi-service runtime
PostgreSQL dependency
Redis dependency
GitHub Actions CI
Local Kubernetes deployment
Kubernetes probes
API pod failure testing
Two-replica resilience improvement
Redis dependency failure testing
PostgreSQL dependency failure testing
Reusable availability testing script
Prometheus metrics
Dependency health metric
Grafana dashboard
Grafana Dependency Health panel
Screenshot evidence
Six incident reports
Updated README and roadmap documentation
```

---

## Recommended Next Step

The recommended next step is:

```text
Milestone 9 — Automated Chaos Experiments
```

This would build naturally on the current observability work.

The strongest next improvement would be to move from manual failure testing toward automated chaos experiments using a tool such as LitmusChaos or Chaos Mesh.

---

## Roadmap Notes

This roadmap should continue to evolve as new experiments are added.

The project should keep following this pattern:

```text
Make a change
Run a test
Capture evidence
Document the result
Update the README
Commit and push
Confirm GitHub Actions
```

This keeps the repository clean, reviewable, and portfolio-ready.
