[![CI - API Tests and Docker Build](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-health%20API-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/docker%20compose-API%20%7C%20PostgreSQL%20%7C%20Redis-2496ED.svg)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-dependency%20check-4169E1.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-cache%20failure%20test-DC382D.svg)](https://redis.io/)
[![Pytest](https://img.shields.io/badge/tests-pytest%20passing-success.svg)](https://docs.pytest.org/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)](https://github.com/features/actions)
[![Kubernetes](https://img.shields.io/badge/kubernetes-planned-326CE5.svg)](https://kubernetes.io/)
[![Prometheus](https://img.shields.io/badge/prometheus-planned-E6522C.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/grafana-planned-F46800.svg)](https://grafana.com/)
[![Chaos Engineering](https://img.shields.io/badge/chaos%20engineering-first%20failure%20test-critical.svg)](#first-resilience-test)
[![Status](https://img.shields.io/badge/project-active%20development-success.svg)](#current-project-status)

# ⚡ Chaos Engineering Sandbox — DevOps Reliability Portfolio Project

A hands-on DevOps and Cloud Support portfolio project focused on **building, monitoring, breaking, recovering, and improving** a cloud-native system.

This project demonstrates practical skills in **FastAPI, Docker, Docker Compose, PostgreSQL, Redis, automated testing, GitHub Actions CI, dependency readiness checks, and incident-style reliability documentation**.

The long-term goal is to build a Kubernetes-based chaos engineering sandbox where controlled failures can be injected into a microservices environment, measured through observability tools, and documented through clear case studies.

---

## 📋 Table of Contents

- [Current Project Status](#current-project-status)
- [Project Overview](#project-overview)
- [Why I Built This](#why-i-built-this)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Current API Endpoints](#current-api-endpoints)
- [Dependency Readiness Checks](#dependency-readiness-checks)
- [First Resilience Test](#first-resilience-test)
- [Tech Stack](#tech-stack)
- [Local Development Setup](#local-development-setup)
- [Run Tests](#run-tests)
- [Docker Build and Local Test](#docker-build-and-local-test)
- [Docker Compose Multi-Service Setup](#docker-compose-multi-service-setup)
- [GitHub Actions CI](#github-actions-ci)
- [Chaos Engineering Roadmap](#chaos-engineering-roadmap)
- [Observability Roadmap](#observability-roadmap)
- [Project Structure](#project-structure)
- [DevOps and Cloud Skills Demonstrated](#devops-and-cloud-skills-demonstrated)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

---

## ✅ Current Project Status

The project has completed the initial foundation, backend API setup, automated tests, Docker containerization, Docker Compose multi-service setup, PostgreSQL and Redis readiness checks, a manual Redis failure test, incident report documentation, and GitHub Actions CI validation.

| Area | Status |
|---|---|
| Public GitHub repository | Completed |
| Project structure | Completed |
| Portfolio-style README | Updated |
| Architecture notes | Completed |
| Project roadmap | Completed |
| FastAPI backend service | Completed |
| API health endpoint | Completed |
| API readiness endpoint | Completed |
| API status endpoint | Completed |
| Work simulation endpoint | Completed |
| Pytest automated tests | Completed |
| `pytest.ini` configuration | Completed |
| GitHub Actions test workflow | Completed |
| GitHub Actions Docker build check | Completed |
| Dockerfile for API service | Completed |
| `.dockerignore` | Completed |
| Docker Compose for API service | Completed |
| PostgreSQL Docker Compose service | Completed |
| Redis Docker Compose service | Completed |
| PostgreSQL readiness check | Completed |
| Redis readiness check | Completed |
| Manual Redis failure test | Completed |
| First incident report | Completed |
| Kubernetes manifests | Planned |
| Prometheus metrics | Planned |
| Grafana dashboards | Planned |
| Kubernetes chaos experiments | Planned |
| Current working branch | `main` |

---

## 📖 Project Overview

The **Chaos Engineering Sandbox** is a learning and portfolio project that explores how modern cloud-native systems behave under failure.

Instead of only building an application that works under normal conditions, this project aims to answer more realistic engineering questions:

- What happens if a service crashes?
- What happens if a dependency becomes unavailable?
- What happens if response time becomes slow?
- Can the system recover automatically?
- How long does recovery take?
- What metrics prove that recovery happened?
- What should be improved after each failure test?

The project starts with a FastAPI backend and gradually evolves into a microservices-style environment with Docker, PostgreSQL, Redis, Kubernetes, Prometheus, Grafana, and controlled chaos experiments.

---

## 🎯 Why I Built This

I built this project to strengthen my DevOps and Cloud Support skills through a realistic reliability-focused workflow.

In real production environments, failure is unavoidable. Containers may restart, databases may slow down, cache services may become unavailable, networks may become unreliable, and users may be affected before engineers notice the problem.

This sandbox gives me a safe environment to practise:

- Building cloud-native services
- Writing automated tests
- Containerising applications
- Running multiple services locally
- Creating CI pipelines
- Checking dependency readiness
- Preparing Kubernetes deployments
- Monitoring system behaviour
- Injecting controlled failures
- Measuring recovery time
- Writing incident-style documentation
- Improving the system after each test

The goal is to show not only that I can deploy an application, but that I can understand, troubleshoot, document, and improve system reliability.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **FastAPI Backend** | Lightweight API service used as the first application component |
| **Health Endpoint** | `/health` confirms that the API process is alive |
| **Readiness Endpoint** | `/ready` checks whether PostgreSQL and Redis are reachable |
| **Status Endpoint** | `/status` shows feature and dependency status |
| **Work Simulation Endpoint** | `/simulate-work` creates variable processing time for later monitoring |
| **PostgreSQL Dependency** | Simulates a real database dependency |
| **Redis Dependency** | Simulates a cache dependency and supports failure testing |
| **Automated Tests** | Pytest validates all current API endpoints |
| **Dockerized API** | API service can be built and run as a Docker container |
| **Docker Compose Stack** | API, PostgreSQL, and Redis can run together with one command |
| **GitHub Actions CI** | Automatically runs tests and Docker build checks on push |
| **Incident Report Documentation** | First failure test documented as a reliability case study |
| **Architecture Documentation** | Notes explain current and planned system design |
| **Chaos Engineering Roadmap** | Planned experiments include pod kill, latency injection, Redis failure, and database failure |

---

## 🏗️ Architecture

### Current Local Development Architecture

```text
┌────────────────────┐
│ Local Developer    │
│ VS Code + Git      │
└─────────┬──────────┘
          │ code + commit
          ▼
┌────────────────────┐
│ FastAPI Backend    │
│ app/api/main.py    │
└─────────┬──────────┘
          │ exposes
          ▼
┌────────────────────┐
│ API Endpoints      │
│ /health /ready     │
│ /status /docs      │
└────────────────────┘
```

### Current Docker Compose Architecture

```text
┌─────────────────────────────┐
│ Local Machine               │
│ Docker Desktop              │
└──────────────┬──────────────┘
               │ docker compose up --build
               ▼
┌─────────────────────────────┐
│ Docker Compose Network      │
├─────────────────────────────┤
│ chaos-api                   │
│ FastAPI + Uvicorn           │
│ Port: 8000                  │
├─────────────────────────────┤
│ chaos-postgres              │
│ PostgreSQL database         │
│ Port: 5432                  │
├─────────────────────────────┤
│ chaos-redis                 │
│ Redis cache                 │
│ Port: 6379                  │
└──────────────┬──────────────┘
               │ browser / curl
               ▼
┌─────────────────────────────┐
│ http://127.0.0.1:8000       │
│ /health /ready /status      │
└─────────────────────────────┘
```

### Dependency Flow

```text
Browser / curl
     │
     ▼
FastAPI API
     │
     ├── checks PostgreSQL with SELECT 1
     │
     └── checks Redis with PING
```

### Planned Kubernetes Architecture

```text
┌────────────────────┐
│ User / Browser     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Frontend Service   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Backend API        │
│ FastAPI            │
└──────┬───────┬─────┘
       │       │
       ▼       ▼
┌──────────┐ ┌──────────┐
│PostgreSQL│ │ Redis    │
│Database  │ │ Cache    │
└──────────┘ └──────────┘
       │       │
       └───┬───┘
           ▼
┌────────────────────┐
│ Kubernetes Cluster │
│ Probes + Services  │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Observability      │
│ Prometheus/Grafana │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Chaos Experiments  │
│ LitmusChaos/Mesh   │
└────────────────────┘
```

---

## 📡 Current API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | `GET` | Root project message |
| `/health` | `GET` | Confirms the API service is alive |
| `/ready` | `GET` | Confirms whether API dependencies are reachable |
| `/status` | `GET` | Shows current service, feature, and dependency status |
| `/simulate-work` | `GET` | Simulates variable work for future monitoring tests |
| `/docs` | `GET` | FastAPI interactive API documentation |

Example `/health` response:

```json
{
  "status": "healthy",
  "service": "chaos-api",
  "timestamp": "2026-06-05T00:00:00+00:00"
}
```

Example `/ready` response when all dependencies are reachable:

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
  },
  "timestamp": "2026-06-05T00:00:00+00:00"
}
```

Example `/ready` response when Redis is stopped:

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
      "message": "Error 111 connecting to redis:6379. Connection refused."
    }
  },
  "timestamp": "2026-06-05T00:00:00+00:00"
}
```

---

## 🔎 Dependency Readiness Checks

The project now distinguishes between **health** and **readiness**.

| Check | Endpoint | Meaning |
|---|---|---|
| Health check | `/health` | The API process is alive |
| Readiness check | `/ready` | The API can reach its required dependencies |
| Status check | `/status` | Shows feature flags and dependency details |

This matters because a service can be alive but not ready.

For example, if the API process is running but Redis is unavailable, `/health` can still return healthy while `/ready` correctly reports that the system is not ready.

This mirrors real Kubernetes behaviour where readiness probes help prevent traffic from being sent to pods that are alive but not ready to serve requests.

---

## 🧪 First Resilience Test

The first manual failure test simulated a Redis cache outage.

### Test Summary

| Item | Result |
|---|---|
| Failure injected | Redis container stopped manually |
| Command used | `docker stop chaos-redis` |
| API stayed alive | Yes |
| `/ready` detected Redis failure | Yes |
| System changed to `not_ready` | Yes |
| Redis restarted successfully | Yes |
| System returned to `ready` | Yes |
| Incident report created | Yes |

### Failure Command

```bash
docker stop chaos-redis
```

### Recovery Command

```bash
docker start chaos-redis
```

### Incident Report

The full report is documented here:

```text
docs/incident-reports/01-redis-manual-failure-test.md
```

This is the first portfolio evidence that the system can detect a dependency failure and report degraded readiness instead of pretending everything is fine.

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Backend API | Python, FastAPI |
| ASGI Server | Uvicorn |
| Database | PostgreSQL |
| Cache | Redis |
| PostgreSQL Driver | Psycopg 3 |
| Redis Client | redis-py |
| Automated Testing | pytest, FastAPI TestClient, httpx |
| Containers | Docker |
| Local Multi-Service Runtime | Docker Compose |
| CI | GitHub Actions |
| Planned Orchestration | Kubernetes |
| Planned Observability | Prometheus, Grafana |
| Planned Chaos Tooling | LitmusChaos or Chaos Mesh |
| Documentation | Markdown |

---

## 💻 Local Development Setup

### Prerequisites

Install the following tools:

- Git
- Python 3.12 or later
- Docker Desktop
- VS Code or another code editor

> Note: The project CI uses Python 3.12. If your local machine uses a newer Python version and a package install fails, compare it against the CI version or recreate your virtual environment with Python 3.12.

### 1. Clone the Repository

```bash
git clone https://github.com/AnarkeyV/chaos-engineering-sandbox.git
cd chaos-engineering-sandbox
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r app/api/requirements.txt
```

### 5. Run the API Locally with Python

```bash
uvicorn app.api.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

Useful links:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/ready
http://127.0.0.1:8000/status
http://127.0.0.1:8000/simulate-work
http://127.0.0.1:8000/docs
```

> When running only the API locally without Docker Compose, `/ready` may show PostgreSQL and Redis as unreachable. That is expected unless those services are also running locally.

---

## ✅ Run Tests

Run tests from the project root:

```bash
pytest
```

Expected result:

```text
5 passed
```

The current tests validate:

| Test Area | Coverage |
|---|---|
| Root endpoint | Confirms project message and docs link |
| Health endpoint | Confirms API process health response |
| Readiness endpoint | Confirms dependency status structure |
| Status endpoint | Confirms service, feature, and dependency structure |
| Work simulation endpoint | Confirms simulated work response |

---

## 🐳 Docker Build and Local Test

### Build the Docker Image

```bash
docker build -t chaos-api:0.1.0 -f app/api/Dockerfile .
```

### Run the Container

```bash
docker run --name chaos-api-container -p 8000:8000 chaos-api:0.1.0
```

Open:

```text
http://127.0.0.1:8000/health
```

### Stop the Container

Press:

```text
Control + C
```

Then remove the container:

```bash
docker rm chaos-api-container
```

---

## 🧱 Docker Compose Multi-Service Setup

Docker Compose is the recommended way to run the current project locally because it starts the API, PostgreSQL, and Redis together.

### Start the Full Stack

```bash
docker compose up --build
```

Expected containers:

```text
chaos-api
chaos-postgres
chaos-redis
```

### Check Running Containers

Open a second terminal tab and run:

```bash
docker ps
```

### Test Readiness

Open:

```text
http://127.0.0.1:8000/ready
```

Expected dependency status:

```text
PostgreSQL: reachable
Redis: reachable
```

### Test Status

Open:

```text
http://127.0.0.1:8000/status
```

Expected feature status:

```json
"features": {
  "database": true,
  "cache": true,
  "observability": false,
  "chaos_experiments": false
}
```

### Stop the Full Stack

Press:

```text
Control + C
```

Then run:

```bash
docker compose down
```

To remove the PostgreSQL volume as well, use this only when you intentionally want to delete local database data:

```bash
docker compose down -v
```

---

## 🔄 GitHub Actions CI

The workflow file is located at:

```text
.github/workflows/ci.yml
```

The current CI workflow runs on pushes and pull requests to `main`.

Pipeline flow:

```text
Code pushed to GitHub
 ↓
Checkout repository
 ↓
Set up Python 3.12
 ↓
Install dependencies
 ↓
Run pytest
 ↓
Build Docker image
 ↓
Pass or fail workflow
```

Current CI jobs:

| Job | Purpose |
|---|---|
| `Run FastAPI Tests` | Runs pytest against the API |
| `Build Docker Image` | Confirms the API Docker image can build successfully |

This gives the repository an early DevOps quality gate before Kubernetes, observability, and chaos experiments are added.

---

## 🔥 Chaos Engineering Roadmap

The current Redis failure test is a manual dependency failure check. Later milestones will move into Kubernetes-based chaos experiments.

| Experiment | Stage | Purpose |
|---|---|---|
| Redis manual failure | Completed | Confirm API readiness changes when cache fails |
| API container restart | Planned | Observe API recovery after process/container restart |
| PostgreSQL failure | Planned | Confirm API detects database outage |
| API pod kill | Planned | Test Kubernetes pod recovery |
| Redis pod kill | Planned | Test cache dependency failure inside Kubernetes |
| Network latency injection | Planned | Measure slower service response |
| CPU stress | Planned | Observe resource pressure impact |
| Memory stress | Planned | Observe memory pressure and recovery |

Each chaos experiment should include:

```text
Hypothesis
Failure injected
Expected result
Actual result
Recovery action
Recovery time
Lessons learned
Improvement made
```

---

## 📊 Observability Roadmap

Observability will be added before full chaos engineering experiments.

Planned monitoring areas:

| Area | Planned Tooling |
|---|---|
| Application metrics | Prometheus client metrics |
| Container metrics | Docker/Kubernetes metrics |
| Dashboards | Grafana |
| Availability | Health and readiness panels |
| Latency | Request duration panels |
| Dependency status | PostgreSQL and Redis status indicators |
| Recovery tracking | Failure and recovery timeline |

Planned dashboard panels:

```text
API uptime
Request count
Request latency
Error rate
PostgreSQL readiness
Redis readiness
Pod restart count
CPU usage
Memory usage
Recovery timeline
```

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
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/
├── docs/
│   ├── project-roadmap.md
│   ├── architecture-notes.md
│   └── incident-reports/
│       └── 01-redis-manual-failure-test.md
├── tests/
│   └── test_api.py
├── k8s/
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
| Version Control | Git, GitHub, clean commits, public repo structure |
| API Development | FastAPI, Uvicorn, health/readiness/status endpoints |
| Automated Testing | pytest, FastAPI TestClient |
| Dependency Management | Python requirements, virtual environment |
| Containerisation | Dockerfile, Docker image build, local container run |
| Multi-Service Runtime | Docker Compose with API, PostgreSQL, and Redis |
| Database Connectivity | PostgreSQL readiness check using Psycopg 3 |
| Cache Connectivity | Redis readiness check using ping |
| CI/CD Foundation | GitHub Actions tests and Docker build validation |
| Reliability Thinking | Health vs readiness distinction |
| Failure Testing | Manual Redis outage and recovery test |
| Incident Documentation | Incident-style report for dependency failure |
| Portfolio Documentation | README, roadmap, architecture notes, incident reports |

---

## 🔮 Future Improvements

Planned next improvements:

- Add PostgreSQL sample table and simple database read/write route
- Add Redis-backed cache route
- Add Prometheus-compatible metrics endpoint
- Add Grafana dashboard package
- Add Kubernetes manifests for API, PostgreSQL, and Redis
- Add Kubernetes liveness and readiness probes
- Add Kubernetes namespace separation
- Add first Kubernetes pod kill experiment
- Add automated incident report templates
- Add screenshots of failure and recovery evidence
- Add architecture diagram using draw.io
- Add optional Azure AKS or Google GKE deployment
- Add GitHub Actions Docker image publishing later

---

## 👤 Author

**Khairul Rizal**

DevOps and Cloud Support learner building practical portfolio projects focused on cloud-native systems, automation, reliability, and resilience engineering.

---

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

Built as part of a DevOps and Cloud Support learning journey.

Last updated: June 2026
