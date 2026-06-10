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
| Milestone 8 — Alerting and reliability metrics | Planned |
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

## Milestone 8 — Alerting and Reliability Metrics

### Status

Planned

### Objective

Add alerting and reliability-focused signals so the project moves from observation to notification.

### Planned Work

- Add Prometheus alerting rules.
- Add alert for API readiness failures.
- Add alert for high request latency.
- Add alert for failed HTTP requests.
- Add Grafana alerting.
- Add dashboard panels for readiness failure count.
- Add dependency status metrics for PostgreSQL and Redis.
- Add MTTR measurement notes.

### Possible New Metrics

| Metric | Purpose |
|---|---|
| `chaos_api_dependency_up` | Shows whether PostgreSQL and Redis are reachable |
| `chaos_api_readiness_status` | Shows whether the API is ready |
| `chaos_api_dependency_check_duration_seconds` | Measures dependency check latency |

### Expected Outcome

The system should be able to show not only what happened, but also when an operator should be alerted.

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
| Observability | Prometheus metrics and Grafana dashboard |
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
Grafana dashboard
Screenshot evidence
Six incident reports
Updated README and roadmap documentation
```

---

## Recommended Next Step

The recommended next milestone is:

```text
Milestone 8 — Alerting and Reliability Metrics
```

This would build naturally on the current observability work.

The strongest next improvement would be to add a dependency metric such as:

```text
chaos_api_dependency_up{dependency="postgres"}
chaos_api_dependency_up{dependency="redis"}
```

This would allow Grafana and Prometheus to show dependency health directly instead of only inferring dependency failure from `/ready`.

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
