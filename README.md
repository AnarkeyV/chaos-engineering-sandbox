[![CI - API Tests and Docker Build](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-health%20api-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-compose%20%7C%20image%20build-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-kind%20local%20cluster-326CE5.svg)](https://kubernetes.io/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-dependency%20check-336791.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-cache%20failure%20test-DC382D.svg)](https://redis.io/)
[![Status](https://img.shields.io/badge/project-kubernetes%20resilience%20milestone-success.svg)](#current-project-status)

# ⚡ Chaos Engineering Sandbox — DevOps & Cloud Resilience Project

A hands-on DevOps, Cloud Support, and Site Reliability Engineering portfolio project focused on **building, monitoring, breaking, recovering, and improving** a cloud-native system.

This project demonstrates how a small microservices-style application can be containerised with Docker, tested through GitHub Actions, deployed locally with Kubernetes using Kind, connected to PostgreSQL and Redis, and validated through controlled failure testing.

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
- [Docker Build and Local Test](#docker-build-and-local-test)
- [Docker Compose Multi-Service Setup](#docker-compose-multi-service-setup)
- [Dependency Readiness Checks](#dependency-readiness-checks)
- [Kubernetes Local Deployment](#kubernetes-local-deployment)
- [Kubernetes Resilience Tests](#kubernetes-resilience-tests)
- [Incident Reports](#incident-reports)
- [GitHub Actions CI](#github-actions-ci)
- [Project Structure](#project-structure)
- [DevOps and Cloud Skills Demonstrated](#devops-and-cloud-skills-demonstrated)
- [Future Improvements](#future-improvements)
- [Useful Commands](#useful-commands)
- [License](#license)

---

## ✅ Current Project Status

The project has completed the local Docker, Docker Compose, CI, Kubernetes deployment, and early resilience testing milestones.

| Area | Status |
|---|---|
| Public GitHub repository | Completed |
| Portfolio-style README | Updated |
| Project roadmap documentation | Completed |
| Architecture notes | Completed |
| FastAPI backend service | Completed |
| API health/status/readiness endpoints | Completed |
| pytest automated tests | Completed |
| GitHub Actions CI | Passing |
| Dockerfile | Completed |
| Docker image build check in CI | Completed |
| Docker Compose local setup | Completed |
| PostgreSQL service | Added |
| Redis service | Added |
| Docker Compose health checks | Added |
| API dependency checks for PostgreSQL and Redis | Completed |
| Manual Redis failure test | Completed |
| Local Kind Kubernetes cluster | Completed |
| Kubernetes namespace | Completed |
| Kubernetes API Deployment and Service | Completed |
| Kubernetes PostgreSQL Deployment and Service | Completed |
| Kubernetes Redis Deployment and Service | Completed |
| Kubernetes liveness and readiness probes | Completed |
| API pod failure test | Completed |
| API replica improvement from 1 to 2 replicas | Completed |
| Incident-style resilience reports | 3 reports completed |
| Current API image version | `chaos-api:0.2.0` |
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
Can we document the results clearly?
```

The project begins with a small FastAPI service, then gradually evolves into a multi-service system with:

- API service
- PostgreSQL database dependency
- Redis cache dependency
- Docker containerisation
- Docker Compose local orchestration
- GitHub Actions CI
- Kubernetes local deployment using Kind
- Readiness and liveness probes
- Manual failure tests
- Incident-style documentation

---

## 🎯 Why I Built This

I built this project to deepen my understanding of DevOps, Cloud Support, Kubernetes, observability, and reliability engineering.

In real-world systems, failure is unavoidable.

Applications can crash. Containers can stop. Databases can become unavailable. Cache services can fail. Network latency can increase. Deployments can go wrong.

This sandbox allows me to safely test failure scenarios, observe system behavior, and document how the system recovers.

The goal is to build a portfolio project that demonstrates practical skills relevant to:

- DevOps Engineer roles
- Cloud Support Engineer roles
- Platform Engineering roles
- Site Reliability Engineering roles
- Infrastructure and Operations roles

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **FastAPI Backend** | Simple API service used for health, readiness, and failure testing |
| **Health Endpoint** | `/health` confirms that the API process is alive |
| **Readiness Endpoint** | `/ready` checks whether PostgreSQL and Redis are reachable |
| **Status Endpoint** | `/status` shows service version, environment, features, and dependencies |
| **Work Simulation Endpoint** | `/simulate-work` creates artificial processing delay |
| **Automated Tests** | pytest validates API endpoints |
| **GitHub Actions CI** | Runs tests and Docker image build checks on push |
| **Dockerfile** | Packages the API as a container image |
| **Docker Compose** | Runs API, PostgreSQL, and Redis together locally |
| **Docker Compose Health Checks** | Tracks service health for API, PostgreSQL, and Redis |
| **PostgreSQL Dependency** | Simulates a persistent database dependency |
| **Redis Dependency** | Simulates a cache dependency |
| **Manual Redis Failure Test** | Validates that the API detects Redis failure |
| **Kind Kubernetes Cluster** | Runs Kubernetes locally using Docker |
| **Kubernetes Manifests** | Deploys API, PostgreSQL, and Redis to Kubernetes |
| **Liveness Probe** | Helps Kubernetes know whether the API is alive |
| **Readiness Probe** | Helps Kubernetes know whether the API is ready for traffic |
| **API Pod Failure Test** | Demonstrates Kubernetes pod recovery |
| **Replica Improvement** | Scales API from 1 replica to 2 replicas for better resilience |
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
│   │   └── /simulate-work
│   │
│   ├── chaos-postgres
│   │   └── PostgreSQL database dependency
│   │
│   └── chaos-redis
│       └── Redis cache dependency
│
└── Browser / curl
    └── http://127.0.0.1:8000
```

### Current Kubernetes Architecture

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
    │   └── PostgreSQL pod
    │
    ├── Service: postgres
    │   └── ClusterIP service on port 5432
    │
    ├── Deployment: chaos-redis
    │   └── Redis pod
    │
    └── Service: redis
        └── ClusterIP service on port 6379
```

### Kubernetes Traffic Flow

```text
User / Browser
 ↓
kubectl port-forward
 ↓
chaos-api-service
 ↓
chaos-api pods
 ↓
PostgreSQL service
 ↓
PostgreSQL pod

chaos-api pods
 ↓
Redis service
 ↓
Redis pod
```

### Resilience Testing Flow

```text
Deploy system
 ↓
Confirm healthy state
 ↓
Inject controlled failure
 ↓
Observe Kubernetes or API response
 ↓
Confirm recovery
 ↓
Document incident report
 ↓
Improve system design
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
| Containers | Docker |
| Local Multi-Service Runtime | Docker Compose |
| CI | GitHub Actions |
| Local Kubernetes | Kind |
| Kubernetes CLI | kubectl |
| Database | PostgreSQL |
| Cache | Redis |
| Documentation | Markdown |
| Future Observability | Prometheus, Grafana |
| Future Chaos Tooling | LitmusChaos or Chaos Mesh |

---

## 📡 Application Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | `GET` | Root endpoint with API message |
| `/health` | `GET` | Confirms the API process is alive |
| `/ready` | `GET` | Confirms API dependency readiness |
| `/status` | `GET` | Shows API version, environment, features, and dependencies |
| `/simulate-work` | `GET` | Simulates a small amount of processing work |
| `/docs` | `GET` | FastAPI interactive documentation |

### Example `/health` response

```json
{
  "status": "healthy",
  "service": "chaos-api",
  "timestamp": "2026-06-05T09:00:00+00:00"
}
```

### Example `/ready` response when dependencies are reachable

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

### Example `/ready` response when Redis is unavailable

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
      "message": "Error connecting to Redis"
    }
  }
}
```

---

## 💻 Local Development

### Prerequisites

Install the following:

- Git
- Python 3.12 or later
- Docker Desktop
- VS Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/AnarkeyV/chaos-engineering-sandbox.git
cd chaos-engineering-sandbox
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r app/api/requirements.txt
```

### 5. Run the API locally

```bash
uvicorn app.api.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

Useful local URLs:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/ready
http://127.0.0.1:8000/status
http://127.0.0.1:8000/simulate-work
http://127.0.0.1:8000/docs
```

> Note: When running the API directly with Python, PostgreSQL and Redis may not be available unless they are also running locally. In that case, `/ready` may return `not_ready`. This is expected.

---

## ✅ Automated Testing

Tests are located in:

```text
tests/
└── test_api.py
```

Run tests locally:

```bash
pytest
```

Expected result:

```text
5 passed
```

The tests validate:

| Test | Purpose |
|---|---|
| Root endpoint | Confirms `/` returns the correct API message |
| Health endpoint | Confirms `/health` returns healthy status |
| Ready endpoint | Confirms `/ready` returns dependency information |
| Status endpoint | Confirms `/status` returns service and feature information |
| Simulate work endpoint | Confirms `/simulate-work` returns a successful response |

---

## 🐳 Docker Build and Local Test

The API Dockerfile is located at:

```text
app/api/Dockerfile
```

Build the Docker image:

```bash
docker build -t chaos-api:0.2.0 -f app/api/Dockerfile .
```

Run the container:

```bash
docker run --name chaos-api-container -p 8000:8000 chaos-api:0.2.0
```

Open:

```text
http://127.0.0.1:8000/health
```

Stop the container:

```text
Control + C
```

Remove the container:

```bash
docker rm chaos-api-container
```

---

## 🧱 Docker Compose Multi-Service Setup

The Docker Compose file runs:

```text
chaos-api
chaos-postgres
chaos-redis
```

Start the full local system:

```bash
docker compose up --build
```

Check running containers:

```bash
docker compose ps
```

Expected services:

```text
chaos-api
chaos-postgres
chaos-redis
```

Open:

```text
http://127.0.0.1:8000/ready
```

Expected result:

```text
status: ready
database: reachable
cache: reachable
```

Stop the system:

```text
Control + C
```

Clean up:

```bash
docker compose down
```

### Docker Compose Health Checks

The Compose setup includes health checks for:

| Service | Health Check |
|---|---|
| API | Calls `/health` |
| PostgreSQL | Runs `pg_isready` |
| Redis | Runs `redis-cli ping` |

This helps confirm that services are not only running, but also healthy.

---

## 🔍 Dependency Readiness Checks

The API includes real dependency checks for PostgreSQL and Redis.

### PostgreSQL check

The API attempts to connect to PostgreSQL and run:

```sql
SELECT 1;
```

If successful, the database status becomes:

```text
reachable
```

### Redis check

The API attempts to connect to Redis and run:

```text
PING
```

If successful, the cache status becomes:

```text
reachable
```

This distinction is important:

| Endpoint | Meaning |
|---|---|
| `/health` | The API process is alive |
| `/ready` | The API and its dependencies are ready |
| `/status` | The API reports its environment, features, and dependency state |

---

## ☸️ Kubernetes Local Deployment

This project uses **Kind** to run a local Kubernetes cluster.

### 1. Create a Kind cluster

```bash
kind create cluster --name chaos-sandbox
```

Check the node:

```bash
kubectl get nodes
```

Expected result:

```text
STATUS
Ready
```

### 2. Build the API image

```bash
docker build -t chaos-api:0.2.0 -f app/api/Dockerfile .
```

### 3. Load the image into Kind

```bash
kind load docker-image chaos-api:0.2.0 --name chaos-sandbox
```

### 4. Apply Kubernetes manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
```

### 5. Check pods

```bash
kubectl get pods -n chaos-sandbox
```

Expected result:

```text
chaos-api-xxxxx        1/1 Running
chaos-api-yyyyy        1/1 Running
chaos-postgres-xxxxx   1/1 Running
chaos-redis-xxxxx      1/1 Running
```

### 6. Check Deployment

```bash
kubectl get deployment chaos-api -n chaos-sandbox
```

Expected current result:

```text
NAME        READY   UP-TO-DATE   AVAILABLE
chaos-api   2/2     2            2
```

### 7. Access the API using port-forwarding

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

Open:

```text
http://127.0.0.1:8000/ready
```

More details are documented in:

[docs/kubernetes-local-deployment.md](docs/kubernetes-local-deployment.md)

---

## 🧪 Kubernetes Resilience Tests

The project now includes early manual resilience tests.

### Test 1: Redis Manual Failure Test

Redis was stopped manually using Docker:

```bash
docker stop chaos-redis
```

Result:

| Check | Result |
|---|---|
| API stayed alive | Yes |
| Redis failure detected | Yes |
| `/ready` changed to `not_ready` | Yes |
| Redis recovery detected | Yes |

Report:

[docs/incident-reports/01-redis-manual-failure-test.md](docs/incident-reports/01-redis-manual-failure-test.md)

---

### Test 2: Kubernetes API Pod Failure Test

The API pod was manually deleted:

```bash
kubectl delete pod <API_POD_NAME> -n chaos-sandbox
```

Result:

| Check | Result |
|---|---|
| API pod deleted | Yes |
| Kubernetes created a replacement pod | Yes |
| Deployment returned to available state | Yes |
| PostgreSQL remained running | Yes |
| Redis remained running | Yes |

Key evidence:

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

Report:

[docs/incident-reports/02-kubernetes-api-pod-failure-test.md](docs/incident-reports/02-kubernetes-api-pod-failure-test.md)

---

### Test 3: API Replica Resilience Improvement

The API Deployment was improved from one replica to two replicas.

Before:

```yaml
replicas: 1
```

After:

```yaml
replicas: 2
```

Current evidence:

```text
Replicas: 2 desired | 2 updated | 2 total | 2 available | 0 unavailable
```

Result:

| Check | Result |
|---|---|
| API replica count increased | Yes |
| Two API pods running | Yes |
| Deployment returned `2/2` ready | Yes |
| Resilience improved | Yes |

Report:

[docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md](docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md)

---

## 📄 Incident Reports

Incident reports are stored in:

```text
docs/incident-reports/
```

Current reports:

| Report | Description |
|---|---|
| [01 Redis Manual Failure Test](docs/incident-reports/01-redis-manual-failure-test.md) | Documents API behavior when Redis is stopped |
| [02 Kubernetes API Pod Failure Test](docs/incident-reports/02-kubernetes-api-pod-failure-test.md) | Documents Kubernetes recovery after API pod deletion |
| [03 Kubernetes API Replica Resilience Improvement](docs/incident-reports/03-kubernetes-api-replica-resilience-improvement.md) | Documents scaling API replicas from 1 to 2 |

These reports follow an incident-style format:

```text
Experiment name
Purpose
Hypothesis
Failure injected
Expected result
Actual result
Recovery evidence
Lessons learned
Future improvement
```

---

## 🔄 GitHub Actions CI

The workflow file is located at:

```text
.github/workflows/ci.yml
```

The CI workflow runs on:

```text
push to main
pull request to main
```

The workflow performs:

1. Checkout repository
2. Set up Python
3. Install dependencies
4. Run pytest
5. Build Docker image

Current workflow logic:

```text
Code pushed to GitHub
 ↓
Run API tests
 ↓
Build Docker image
 ↓
Pass or fail workflow
```

This validates that the API still works and the Docker image can be built successfully.

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
│       └── 03-kubernetes-api-replica-resilience-improvement.md
├── k8s/
│   ├── namespace.yaml
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── redis-deployment.yaml
│   └── redis-service.yaml
├── observability/
├── chaos/
├── scripts/
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
| API Health Design | `/health`, `/ready`, `/status` |
| Automated Testing | pytest |
| CI | GitHub Actions |
| Containerisation | Docker, Dockerfile |
| Local Orchestration | Docker Compose |
| Databases | PostgreSQL dependency check |
| Caching | Redis dependency check |
| Kubernetes | Kind, kubectl, Namespace, Deployment, Service |
| Reliability | Liveness probes, readiness probes, replicas |
| Failure Testing | Redis failure, API pod deletion |
| Recovery Analysis | Kubernetes desired state and pod recreation |
| Resilience Improvement | API scaled from 1 replica to 2 replicas |
| Incident Documentation | Failure reports, lessons learned, improvements |
| Cloud Support Thinking | Diagnosis, dependency checks, recovery evidence |
| SRE Thinking | Availability, readiness, resilience, MTTR preparation |

---

## 🔮 Future Improvements

Planned next steps:

- Repeat pod failure test with two API replicas while continuously sending requests.
- Add a simple request loop script to observe availability during failure.
- Add Kubernetes Redis failure test.
- Add Kubernetes PostgreSQL failure test.
- Add Prometheus for metrics collection.
- Add Grafana dashboards.
- Add application metrics endpoint.
- Add visual screenshots to documentation.
- Add LitmusChaos or Chaos Mesh for automated chaos experiments.
- Add Helm charts.
- Add Azure AKS deployment.
- Add Google Kubernetes Engine or Cloud Run optional deployment.
- Add alerting rules for failure detection.
- Add MTTR measurement.
- Add service-level indicators such as availability and latency.
- Add a final case study report.

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

### Create Kind cluster

```bash
kind create cluster --name chaos-sandbox
```

### Build API image

```bash
docker build -t chaos-api:0.2.0 -f app/api/Dockerfile .
```

### Load image into Kind

```bash
kind load docker-image chaos-api:0.2.0 --name chaos-sandbox
```

### Apply Kubernetes manifests

```bash
kubectl apply -f k8s/
```

### Check Kubernetes pods

```bash
kubectl get pods -n chaos-sandbox
```

### Check Kubernetes services

```bash
kubectl get svc -n chaos-sandbox
```

### Check API Deployment

```bash
kubectl get deployment chaos-api -n chaos-sandbox
```

### Describe API Deployment

```bash
kubectl describe deployment chaos-api -n chaos-sandbox
```

### Port-forward API service

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

### Delete one API pod for testing

```bash
kubectl delete pod <API_POD_NAME> -n chaos-sandbox
```

### Watch pods recover

```bash
kubectl get pods -n chaos-sandbox -w
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
Document resilience improvement
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
