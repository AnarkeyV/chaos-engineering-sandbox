[![CI - API Tests and Docker Build](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-health%20api-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-compose%20%7C%20image%20build-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-kind%20local%20cluster-326CE5.svg)](https://kubernetes.io/)
[![Prometheus](https://img.shields.io/badge/prometheus-metrics%20scraping-E6522C.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/grafana-observability%20dashboard-F46800.svg)](https://grafana.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-dependency%20check-336791.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-cache%20failure%20test-DC382D.svg)](https://redis.io/)
[![Availability Test](https://img.shields.io/badge/availability%20test-100%25%20success-success.svg)](#reusable-availability-test-script)
[![Status](https://img.shields.io/badge/project-observability%20milestone%20complete-success.svg)](#current-project-status)

# ⚡ Chaos Engineering Sandbox — DevOps, Kubernetes & Observability Project

A hands-on DevOps, Cloud Support, and Site Reliability Engineering portfolio project focused on **building, monitoring, breaking, recovering, validating, and improving** a cloud-native system.

This project demonstrates how a small microservices-style application can be containerised with Docker, tested through GitHub Actions, deployed locally with Kubernetes using Kind, connected to PostgreSQL and Redis, monitored with Prometheus and Grafana, and validated through controlled failure testing.

---

## 📋 Table of Contents

- [Current Project Status](#current-project-status)
- [Project Overview](#project-overview)
- [Why I Built This](#why-i-built-this)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Application Endpoints](#application-endpoints)
- [Local Development](#local-development)
- [Automated Testing](#automated-testing)
- [Docker Compose Multi-Service Setup](#docker-compose-multi-service-setup)
- [Kubernetes Local Deployment](#kubernetes-local-deployment)
- [Kubernetes Resilience Tests](#kubernetes-resilience-tests)
- [Reusable Availability Test Script](#reusable-availability-test-script)
- [Observability with Prometheus and Grafana](#observability-with-prometheus-and-grafana)
- [Grafana Dashboard](#grafana-dashboard)
- [Incident Reports](#incident-reports)
- [GitHub Actions CI](#github-actions-ci)
- [Project Structure](#project-structure)
- [DevOps and Cloud Skills Demonstrated](#devops-and-cloud-skills-demonstrated)
- [Future Improvements](#future-improvements)
- [Useful Commands](#useful-commands)
- [License](#license)

---

## ✅ Current Project Status

The project has completed local Docker, Docker Compose, CI, Kubernetes deployment, resilience testing, reusable availability testing, and observability milestones.

| Area | Status |
|---|---|
| Public GitHub repository | Completed |
| FastAPI backend service | Completed |
| API health/status/readiness endpoints | Completed |
| API `/metrics` endpoint | Completed |
| pytest automated tests | Completed |
| GitHub Actions CI | Passing |
| Dockerfile | Completed |
| Docker Compose local setup | Completed |
| PostgreSQL service | Added |
| Redis service | Added |
| API dependency checks for PostgreSQL and Redis | Completed |
| Local Kind Kubernetes cluster | Completed |
| Kubernetes API, PostgreSQL, and Redis manifests | Completed |
| Kubernetes liveness and readiness probes | Completed |
| API pod failure test | Completed |
| API replica improvement from 1 to 2 replicas | Completed |
| Two-replica live availability test | Passed — 60/60 HTTP 200 responses |
| Reusable availability test script | Completed |
| Prometheus service | Completed |
| Prometheus API metrics scraping | Completed |
| Grafana service | Completed |
| Grafana Prometheus datasource | Completed |
| Grafana observability dashboard | Completed |
| Dashboard JSON export | Completed |
| Incident-style resilience reports | 4 reports completed |
| Current API image version | `chaos-api:0.3.0` |
| Current API replicas in Kubernetes | `2` |

---

## 📖 Project Overview

The Chaos Engineering Sandbox is a practical learning project designed to demonstrate how modern cloud-native systems behave under failure.

Instead of only proving that an application works, this project focuses on:

```text
Can the system detect failure?
Can the system recover?
Can we observe what happened?
Can we improve the design after testing?
Can users still reach the service while recovery happens?
Can we repeat the test using a reusable script?
Can we visualise system behaviour using monitoring tools?
Can we document the results clearly?
```

The project begins with a small FastAPI service, then gradually evolves into a multi-service system with Docker Compose, Kubernetes, Prometheus, Grafana, and documented failure experiments.

---

## 🎯 Why I Built This

I built this project to deepen my understanding of DevOps, Cloud Support, Kubernetes, observability, and reliability engineering.

In real-world systems, failure is unavoidable. Applications can crash, containers can stop, databases can become unavailable, cache services can fail, latency can increase, and deployments can go wrong.

This sandbox allows me to safely test failure scenarios, observe system behavior, improve the design, and document how the system recovers.

The goal is to build a portfolio project that demonstrates practical skills relevant to DevOps, Cloud Support, Platform Engineering, Site Reliability Engineering, and Infrastructure Operations roles.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **FastAPI Backend** | Simple API service used for health, readiness, metrics, and failure testing |
| **Health Endpoint** | `/health` confirms that the API process is alive |
| **Readiness Endpoint** | `/ready` checks whether PostgreSQL and Redis are reachable |
| **Status Endpoint** | `/status` shows service version, environment, features, and dependencies |
| **Metrics Endpoint** | `/metrics` exposes Prometheus-compatible metrics |
| **Work Simulation Endpoint** | `/simulate-work` creates artificial processing delay |
| **Automated Tests** | pytest validates API endpoints |
| **GitHub Actions CI** | Runs tests and Docker image build checks on push |
| **Docker Compose** | Runs API, PostgreSQL, Redis, Prometheus, and Grafana locally |
| **PostgreSQL Dependency** | Simulates a persistent database dependency |
| **Redis Dependency** | Simulates a cache dependency |
| **Kind Kubernetes Cluster** | Runs Kubernetes locally using Docker |
| **Kubernetes Manifests** | Deploys API, PostgreSQL, and Redis to Kubernetes |
| **Liveness Probe** | Helps Kubernetes know whether the API is alive |
| **Readiness Probe** | Helps Kubernetes know whether the API is ready for traffic |
| **API Pod Failure Test** | Demonstrates Kubernetes pod recovery |
| **Replica Improvement** | Scales API from 1 replica to 2 replicas for better resilience |
| **Live Availability Test** | Sends requests while deleting one API pod |
| **Reusable Test Script** | Automates request checks and prints success/failure summary |
| **Prometheus Monitoring** | Scrapes and stores API metrics |
| **Grafana Dashboard** | Visualises request count, request rate, latency, and active requests |
| **Incident Reports** | Documents failure tests, results, lessons learned, and improvements |

---

## 🏗️ Architecture

### Current Docker Compose Architecture

```text
Local Machine
│
├── Docker Compose
│   │
│   ├── chaos-api
│   │   ├── /health
│   │   ├── /ready
│   │   ├── /status
│   │   ├── /metrics
│   │   └── /simulate-work
│   │
│   ├── chaos-postgres
│   │   └── PostgreSQL database dependency
│   │
│   ├── chaos-redis
│   │   └── Redis cache dependency
│   │
│   ├── chaos-prometheus
│   │   └── Scrapes chaos-api:/metrics
│   │
│   └── chaos-grafana
│       └── Visualises Prometheus metrics
│
└── Browser / curl
    ├── API:        http://127.0.0.1:8000
    ├── Prometheus: http://127.0.0.1:9090
    └── Grafana:    http://127.0.0.1:3000
```

### Kubernetes Architecture

```text
Kind Local Kubernetes Cluster
│
└── Namespace: chaos-sandbox
    │
    ├── Deployment: chaos-api
    │   ├── Replica 1: chaos-api pod
    │   ├── Replica 2: chaos-api pod
    │   ├── Liveness probe: /health
    │   └── Readiness probe: /ready
    │
    ├── Service: chaos-api-service
    │   └── ClusterIP service on port 8000
    │
    ├── Deployment: chaos-postgres
    ├── Service: postgres
    ├── Deployment: chaos-redis
    └── Service: redis
```

### Observability Flow

```text
User / curl / availability script
 ↓
chaos-api
 ↓
/metrics endpoint
 ↓
Prometheus scrapes metrics
 ↓
Grafana queries Prometheus
 ↓
Dashboard visualises API behaviour
```

### Resilience Testing Flow

```text
Deploy system
 ↓
Confirm healthy state
 ↓
Inject controlled failure
 ↓
Send or observe requests during failure
 ↓
Confirm recovery
 ↓
Observe metrics
 ↓
Document evidence
 ↓
Improve system design
 ↓
Automate repeatable validation
```

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Backend API | Python, FastAPI |
| API Server | Uvicorn |
| Testing | pytest, FastAPI TestClient, httpx |
| PostgreSQL Driver | Psycopg 3 |
| Cache Client | redis-py |
| Metrics Client | prometheus-client |
| Containers | Docker |
| Local Multi-Service Runtime | Docker Compose |
| CI | GitHub Actions |
| Local Kubernetes | Kind |
| Kubernetes CLI | kubectl |
| Database | PostgreSQL |
| Cache | Redis |
| Monitoring | Prometheus |
| Dashboarding | Grafana |
| Scripting | Bash, curl, awk |
| Documentation | Markdown |
| Future Chaos Tooling | LitmusChaos or Chaos Mesh |

---

## 📡 Application Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | `GET` | Root endpoint with API message |
| `/health` | `GET` | Confirms the API process is alive |
| `/ready` | `GET` | Confirms API dependency readiness |
| `/status` | `GET` | Shows API version, environment, features, and dependencies |
| `/metrics` | `GET` | Exposes Prometheus-compatible metrics |
| `/simulate-work` | `GET` | Simulates a small amount of processing work |
| `/docs` | `GET` | FastAPI interactive documentation |

### Key custom metrics

| Metric | Purpose |
|---|---|
| `chaos_api_http_requests_total` | Counts API requests by method, endpoint, and status code |
| `chaos_api_http_request_duration_seconds` | Tracks request latency |
| `chaos_api_http_requests_in_progress` | Shows current in-progress API requests |

---

## 💻 Local Development

### Prerequisites

Install Git, Python 3.12 or later, Docker Desktop, and VS Code or another code editor.

### Clone and run locally

```bash
git clone https://github.com/AnarkeyV/chaos-engineering-sandbox.git
cd chaos-engineering-sandbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/api/requirements.txt
uvicorn app.api.main:app --reload --port 8000
```

Useful local URLs:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/ready
http://127.0.0.1:8000/status
http://127.0.0.1:8000/metrics
http://127.0.0.1:8000/simulate-work
http://127.0.0.1:8000/docs
```

---

## ✅ Automated Testing

Run tests locally:

```bash
pytest
```

Expected result:

```text
6 passed
```

The tests validate the root, health, readiness, status, simulate-work, and metrics endpoints.

---

## 🧱 Docker Compose Multi-Service Setup

Start the full local system:

```bash
docker compose up --build
```

Expected services:

```text
chaos-api
chaos-postgres
chaos-redis
chaos-prometheus
chaos-grafana
```

Useful local URLs:

| Service | URL |
|---|---|
| API | `http://127.0.0.1:8000` |
| API metrics | `http://127.0.0.1:8000/metrics` |
| Prometheus | `http://127.0.0.1:9090` |
| Grafana | `http://127.0.0.1:3000` |

Stop the system:

```bash
docker compose down
```

---

## ☸️ Kubernetes Local Deployment

This project uses Kind to run a local Kubernetes cluster.

```bash
kind create cluster --name chaos-sandbox
docker build -t chaos-api:0.2.0 -f app/api/Dockerfile .
kind load docker-image chaos-api:0.2.0 --name chaos-sandbox
kubectl apply -f k8s/
kubectl get pods -n chaos-sandbox
kubectl get deployment chaos-api -n chaos-sandbox
```

Expected current API Deployment result:

```text
NAME        READY   UP-TO-DATE   AVAILABLE
chaos-api   2/2     2            2
```

Access the API using port-forwarding:

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

More details are documented in:

[docs/kubernetes-local-deployment.md](docs/kubernetes-local-deployment.md)

---

## 🧪 Kubernetes Resilience Tests

### Test 1: Redis Manual Failure Test

Redis was stopped manually using Docker. The API stayed alive and `/ready` correctly changed to `not_ready` while Redis was unavailable.

Report:

[docs/incident-reports/01-redis-manual-failure-test.md](docs/incident-reports/01-redis-manual-failure-test.md)

### Test 2: Kubernetes API Pod Failure Test

One API pod was manually deleted. Kubernetes created a replacement pod and restored the Deployment.

Report:

[docs/incident-reports/02-kubernetes-api-pod-failure-test.md](docs/incident-reports/02-kubernetes-api-pod-failure-test.md)

### Test 3: API Replica Resilience Improvement

The API Deployment was improved from one replica to two replicas.

```yaml
replicas: 2
```

Report:

[docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md](docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md)

---

## 🟢 Two-Replica Availability Test

The availability test continuously sent requests to the API while one API pod was deleted.

Result:

| Metric | Result |
|---|---|
| Total requests | `60` |
| Successful responses | `60` |
| Failed responses | `0` |
| Success rate | `100%` |
| Endpoint tested | `/health` |
| API replicas | `2` |

Report:

[docs/incident-reports/04-two-replica-api-availability-test.md](docs/incident-reports/04-two-replica-api-availability-test.md)

---

## 🧰 Reusable Availability Test Script

Script location:

```text
scripts/check_api_availability.sh
```

Make the script executable:

```bash
chmod +x scripts/check_api_availability.sh
```

Run the default test:

```bash
./scripts/check_api_availability.sh
```

Custom usage:

```bash
./scripts/check_api_availability.sh http://127.0.0.1:8000/ready 30 1
```

Script validation results:

| Endpoint | Requests | Successful | Failed | Success Rate | Result |
|---|---:|---:|---:|---:|---|
| `/health` | 60 | 60 | 0 | 100.00% | PASS |
| `/ready` | 30 | 30 | 0 | 100.00% | PASS |

---

## 📊 Observability with Prometheus and Grafana

Observability was added to monitor how the API behaves during normal use and failure testing.

### Prometheus

Prometheus scrapes the API metrics endpoint:

```text
http://api:8000/metrics
```

Configuration file:

```text
observability/prometheus/prometheus.yml
```

Key Prometheus queries:

```promql
chaos_api_http_requests_total
sum(chaos_api_http_requests_total)
rate(chaos_api_http_requests_total[1m])
chaos_api_http_requests_in_progress
```

### Grafana

Grafana is configured with Prometheus as its default datasource.

Datasource file:

```text
observability/grafana/provisioning/datasources/prometheus.yml
```

Local Grafana URL:

```text
http://127.0.0.1:3000
```

Default local login:

```text
Username: admin
Password: admin
```

---

## 📈 Grafana Dashboard

Dashboard name:

```text
Chaos API Observability Dashboard
```

Dashboard export:

```text
observability/grafana/dashboards/chaos-api-observability-dashboard.json
```

Dashboard panels:

| Panel | Purpose |
|---|---|
| Total API Requests | Shows total API request count |
| API Request Rate | Shows requests per second |
| Requests by Endpoint | Shows total requests grouped by endpoint |
| Request Rate by Endpoint | Shows request rate grouped by endpoint |
| 95th Percentile Request Latency | Shows high-percentile API latency |
| In-Progress Requests | Shows active requests currently being processed |

Example dashboard validation traffic:

```bash
./scripts/check_api_availability.sh http://127.0.0.1:8000/health 20 1
./scripts/check_api_availability.sh http://127.0.0.1:8000/ready 20 1
for i in {1..5}; do curl http://127.0.0.1:8000/simulate-work; echo; done
```

Observed validation:

| Endpoint / Action | Result |
|---|---|
| `/health` | 20/20 successful requests |
| `/ready` | 20/20 successful requests |
| `/simulate-work` | 5 successful responses |
| Dashboard | Metrics updated successfully |

---

## 📄 Incident Reports

Incident reports are stored in:

```text
docs/incident-reports/
```

| Report | Description |
|---|---|
| [01 Redis Manual Failure Test](docs/incident-reports/01-redis-manual-failure-test.md) | Documents API behavior when Redis is stopped |
| [02 Kubernetes API Pod Failure Test](docs/incident-reports/02-kubernetes-api-pod-failure-test.md) | Documents Kubernetes recovery after API pod deletion |
| [03 Kubernetes API Replica Resilience Improvement](docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md) | Documents scaling API replicas from 1 to 2 |
| [04 Two-Replica API Availability Test](docs/incident-reports/04-two-replica-api-availability-test.md) | Documents 60/60 successful requests during pod failure |

---

## 🔄 GitHub Actions CI

The workflow file is located at:

```text
.github/workflows/ci.yml
```

The CI workflow performs:

1. Checkout repository
2. Set up Python
3. Install dependencies
4. Run pytest
5. Build Docker image

---

## 📁 Project Structure

```text
chaos-engineering-sandbox/
├── README.md
├── LICENSE
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── pytest.ini
├── app/
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── tests/
│   └── test_api.py
├── docs/
│   ├── architecture-notes.md
│   ├── project-roadmap.md
│   ├── kubernetes-local-deployment.md
│   └── incident-reports/
│       ├── 01-redis-manual-failure-test.md
│       ├── 02-kubernetes-api-pod-failure-test.md
│       ├── 03-kubernetes-api-replica-resilience-improvement.md
│       └── 04-two-replica-api-availability-test.md
├── k8s/
│   ├── namespace.yaml
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── redis-deployment.yaml
│   └── redis-service.yaml
├── scripts/
│   └── check_api_availability.sh
├── observability/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── chaos-api-observability-dashboard.json
│       └── provisioning/
│           └── datasources/
│               └── prometheus.yml
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 📈 DevOps and Cloud Skills Demonstrated

| Skill Area | Tools / Practices |
|---|---|
| Version Control | Git, GitHub, commits, public repository |
| Documentation | README, architecture notes, roadmap, incident reports |
| Backend Development | Python, FastAPI |
| API Health Design | `/health`, `/ready`, `/status`, `/metrics` |
| Automated Testing | pytest |
| CI | GitHub Actions |
| Containerisation | Docker, Dockerfile |
| Local Orchestration | Docker Compose |
| Databases | PostgreSQL dependency check |
| Caching | Redis dependency check |
| Kubernetes | Kind, kubectl, Namespace, Deployment, Service |
| Reliability | Liveness probes, readiness probes, replicas |
| Failure Testing | Redis failure, API pod deletion |
| Availability Testing | 60-request live test during pod failure |
| Scripting | Bash availability test script |
| Monitoring | Prometheus metrics scraping |
| Dashboarding | Grafana dashboard panels |
| Recovery Analysis | Kubernetes desired state and pod recreation |
| Resilience Improvement | API scaled from 1 replica to 2 replicas |
| Incident Documentation | Failure reports, lessons learned, improvements |
| Cloud Support Thinking | Diagnosis, dependency checks, recovery evidence |
| SRE Thinking | Availability, readiness, latency, resilience, observability |

---

## 🔮 Future Improvements

Planned next steps:

- Add Kubernetes Redis failure test.
- Add Kubernetes PostgreSQL failure test.
- Add dashboard screenshots to documentation.
- Add Prometheus alerting rules.
- Add Grafana alerting.
- Add MTTR measurement.
- Add service-level indicators such as availability and latency.
- Add LitmusChaos or Chaos Mesh for automated chaos experiments.
- Add Helm charts.
- Add Azure AKS deployment.
- Add final case study report.

---

## 🧰 Useful Commands

### Run tests

```bash
pytest
```

### Run Docker Compose

```bash
docker compose up --build
```

### Stop Docker Compose

```bash
docker compose down
```

### Open Prometheus

```text
http://127.0.0.1:9090
```

### Open Grafana

```text
http://127.0.0.1:3000
```

### Apply Kubernetes manifests

```bash
kubectl apply -f k8s/
```

### Check Kubernetes pods

```bash
kubectl get pods -n chaos-sandbox
```

### Run reusable availability test

```bash
./scripts/check_api_availability.sh
```

### Generate dashboard traffic

```bash
./scripts/check_api_availability.sh http://127.0.0.1:8000/health 20 1
./scripts/check_api_availability.sh http://127.0.0.1:8000/ready 20 1
for i in {1..5}; do curl http://127.0.0.1:8000/simulate-work; echo; done
```

---

## 🧠 Key Learning Summary

This project currently demonstrates the following learning journey:

```text
Create a basic API
 ↓
Add automated tests
 ↓
Add CI with GitHub Actions
 ↓
Containerise the API
 ↓
Run services with Docker Compose
 ↓
Add PostgreSQL and Redis dependencies
 ↓
Add readiness checks
 ↓
Simulate Redis failure
 ↓
Deploy to local Kubernetes
 ↓
Configure liveness and readiness probes
 ↓
Delete API pod manually
 ↓
Observe Kubernetes recovery
 ↓
Scale API from 1 replica to 2 replicas
 ↓
Send live requests during pod failure
 ↓
Confirm 60/60 successful responses
 ↓
Create reusable availability test script
 ↓
Add Prometheus metrics endpoint
 ↓
Scrape metrics with Prometheus
 ↓
Visualise metrics with Grafana
 ↓
Create observability dashboard
 ↓
Export dashboard as JSON
 ↓
Document resilience and observability improvements
```

This makes the project more than a basic deployment exercise.

It shows the full DevOps and reliability cycle:

```text
Build
Test
Deploy
Break
Recover
Improve
Validate
Observe
Automate
Document
```

---

## 📄 License

This project is licensed under the MIT License.

See:

[LICENSE](LICENSE)

---

Built by **Khairul Rizal** as a DevOps, Cloud Support, and resilience engineering portfolio project.

Last updated: June 2026
