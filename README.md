[![CI - API Tests and Docker Build](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/AnarkeyV/chaos-engineering-sandbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-health%20API-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/docker%20compose-local%20dev-2496ED.svg)](https://docs.docker.com/compose/)
[![Pytest](https://img.shields.io/badge/tests-pytest%20passing-success.svg)](https://docs.pytest.org/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF.svg)](https://github.com/features/actions)
[![Kubernetes](https://img.shields.io/badge/kubernetes-planned-326CE5.svg)](https://kubernetes.io/)
[![Prometheus](https://img.shields.io/badge/prometheus-planned-E6522C.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/grafana-planned-F46800.svg)](https://grafana.com/)
[![Chaos Engineering](https://img.shields.io/badge/chaos%20engineering-sandbox-critical.svg)](#chaos-engineering-roadmap)
[![Status](https://img.shields.io/badge/project-active%20development-success.svg)](#current-project-status)

# ⚡ Chaos Engineering Sandbox — DevOps Reliability Portfolio Project

A hands-on DevOps and Cloud Support portfolio project focused on **building, monitoring, breaking, recovering, and improving** a cloud-native system.

This project is designed to demonstrate practical skills in **FastAPI, Docker, automated testing, CI/CD, Kubernetes, observability, and chaos engineering**. The long-term goal is to create a sandbox where controlled failures can be injected into a microservices environment, measured through monitoring tools, and documented through incident-style reports.

---

## 📋 Table of Contents

- [Current Project Status](#current-project-status)
- [Project Overview](#project-overview)
- [Why I Built This](#why-i-built-this)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Current API Endpoints](#current-api-endpoints)
- [Tech Stack](#tech-stack)
- [Local Development Setup](#local-development-setup)
- [Run Tests](#run-tests)
- [Docker Build and Local Test](#docker-build-and-local-test)
- [Docker Compose](#docker-compose)
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

The project has completed the initial foundation, backend API setup, automated tests, Docker containerization, Docker Compose setup, and GitHub Actions CI validation.

| Area | Status |
|---|---|
| Public GitHub repository | Completed |
| Project structure | Completed |
| README foundation | Updated |
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
| Docker Compose for local API service | Completed |
| PostgreSQL integration | Planned |
| Redis integration | Planned |
| Kubernetes manifests | Planned |
| Prometheus metrics | Planned |
| Grafana dashboards | Planned |
| Chaos experiments | Planned |
| Current working branch | `main` |

---

## 📖 Project Overview

The **Chaos Engineering Sandbox** is a learning and portfolio project that explores how modern systems behave under failure.

Instead of only building an application that works under normal conditions, this project aims to answer more realistic engineering questions:

- What happens if a service crashes?
- What happens if a dependency becomes unavailable?
- What happens if response time becomes slow?
- Can the system recover automatically?
- How long does recovery take?
- What metrics prove that recovery happened?
- What should be improved after each failure test?

The project starts simple with a FastAPI backend and gradually evolves into a microservices-style environment with Docker, Kubernetes, Prometheus, Grafana, and controlled chaos experiments.

---

## 🎯 Why I Built This

I built this project to strengthen my DevOps and Cloud Support skills through a realistic reliability-focused workflow.

In real production environments, failure is unavoidable. Containers may restart, databases may slow down, networks may become unreliable, and users may be affected before engineers notice the problem.

This sandbox gives me a safe environment to practise:

- Building cloud-native services
- Writing automated tests
- Containerising applications
- Creating CI pipelines
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
| **Health Endpoint** | `/health` confirms that the API service is alive |
| **Readiness Endpoint** | `/ready` confirms whether the service is ready to receive traffic |
| **Status Endpoint** | `/status` shows current feature and dependency status |
| **Work Simulation Endpoint** | `/simulate-work` creates variable processing time for later monitoring |
| **Automated Tests** | Pytest validates all current API endpoints |
| **Dockerized API** | API service can be built and run as a Docker container |
| **Docker Compose Support** | Local container startup using one command |
| **GitHub Actions CI** | Automatically runs tests and Docker build checks on push |
| **Architecture Documentation** | Notes explain the planned system design |
| **Chaos Engineering Roadmap** | Planned experiments include pod kill, latency, Redis failure, and database failure |

---

## 🏗️ Architecture

### Current Local Architecture

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

### Current Docker Architecture

```text
┌─────────────────────────┐
│ Local Machine           │
│ Docker Desktop          │
└───────────┬─────────────┘
            │ docker compose up --build
            ▼
┌─────────────────────────┐
│ chaos-api Container     │
│ FastAPI + Uvicorn       │
└───────────┬─────────────┘
            │ port 8000
            ▼
┌─────────────────────────┐
│ Browser / curl          │
│ http://127.0.0.1:8000   │
└─────────────────────────┘
```

### Planned Microservices Architecture

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
```

### Planned Kubernetes, Observability, and Chaos Architecture

```text
┌─────────────────────────────────────┐
│ Kubernetes Cluster                  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Application Namespace          │  │
│  │ - Frontend Pod                 │  │
│  │ - Backend API Pod              │  │
│  │ - PostgreSQL Pod               │  │
│  │ - Redis Pod                    │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Observability Namespace        │  │
│  │ - Prometheus                   │  │
│  │ - Grafana                      │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Chaos Engineering Namespace    │  │
│  │ - LitmusChaos or Chaos Mesh    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 📡 Current API Endpoints

| Endpoint | Method | Purpose | Current Status |
|---|---|---|---|
| `/` | `GET` | Root API message | Working |
| `/health` | `GET` | Confirms API is alive | Working |
| `/ready` | `GET` | Confirms API is ready for traffic | Working |
| `/status` | `GET` | Shows service status and planned feature flags | Working |
| `/simulate-work` | `GET` | Simulates variable processing time | Working |
| `/docs` | `GET` | FastAPI Swagger UI documentation | Working |

Example `/health` response:

```json
{
  "status": "healthy",
  "service": "chaos-api",
  "timestamp": "2026-06-05T00:00:00+00:00"
}
```

Example `/ready` response:

```json
{
  "status": "ready",
  "service": "chaos-api",
  "dependencies": {
    "database": "not_configured_yet",
    "cache": "not_configured_yet"
  },
  "timestamp": "2026-06-05T00:00:00+00:00"
}
```

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Backend API | Python, FastAPI |
| API Server | Uvicorn |
| Testing | Pytest, FastAPI TestClient, HTTPX |
| Containerisation | Docker |
| Local Multi-Container Setup | Docker Compose |
| CI Pipeline | GitHub Actions |
| Version Control | Git, GitHub |
| Documentation | Markdown |
| Planned Database | PostgreSQL |
| Planned Cache | Redis |
| Planned Orchestration | Kubernetes |
| Planned Monitoring | Prometheus, Grafana |
| Planned Chaos Tool | LitmusChaos or Chaos Mesh |
| Planned Cloud Extension | Azure AKS or Google GKE |

---

## 💻 Local Development Setup

### Prerequisites

Before running the project, install:

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

Open the API in your browser:

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

---

## ✅ Run Tests

Run the automated test suite:

```bash
pytest
```

Expected result:

```text
5 passed
```

The tests validate:

| Test | What it checks |
|---|---|
| Root endpoint test | API root message and docs path |
| Health endpoint test | Health status, service name, timestamp |
| Ready endpoint test | Readiness status and dependency placeholders |
| Status endpoint test | Service version, environment, and feature flags |
| Simulate work test | Simulated processing response |

---

## 🐳 Docker Build and Local Test

The Dockerfile is located at:

```text
app/api/Dockerfile
```

### Build the image

Run from the repository root:

```bash
docker build -t chaos-api:0.1.0 -f app/api/Dockerfile .
```

### Run the container

```bash
docker run --name chaos-api-container -p 8000:8000 chaos-api:0.1.0
```

Open:

```text
http://127.0.0.1:8000/health
```

### Stop and remove the container

Stop the running container with:

```text
Control + C
```

Then remove it:

```bash
docker rm chaos-api-container
```

---

## 🧱 Docker Compose

Docker Compose allows the API service to run locally using one command.

The Compose file is located at:

```text
docker-compose.yml
```

### Start the API service

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000/health
```

### Stop the service

Press:

```text
Control + C
```

Then clean up:

```bash
docker compose down
```

---

## 🔄 GitHub Actions CI

The workflow file is located at:

```text
.github/workflows/ci.yml
```

The current CI pipeline runs on every push or pull request to `main`.

### Pipeline Flow

```text
Code pushed to GitHub
        │
        ▼
Checkout repository
        │
        ▼
Set up Python 3.12
        │
        ▼
Install dependencies
        │
        ▼
Run pytest
        │
        ▼
Build Docker image
        │
        ▼
Pass or fail workflow
```

### CI Jobs

| Job | Purpose |
|---|---|
| `Run FastAPI Tests` | Installs dependencies and runs pytest |
| `Build Docker Image` | Builds the API Docker image after tests pass |

This helps ensure that the application code works and the Docker image can be built successfully before more features are added.

---

## ⚡ Chaos Engineering Roadmap

Chaos engineering experiments will be added after the application has multiple services and Kubernetes deployment files.

Planned experiments:

| Experiment | Failure Injected | What It Tests |
|---|---|---|
| API Pod Kill | Deletes or kills API pod | Kubernetes self-healing and recovery time |
| Redis Failure | Cache becomes unavailable | Graceful degradation and dependency handling |
| PostgreSQL Failure | Database becomes unavailable | API error handling and readiness behaviour |
| Network Latency | Adds delay between services | Latency impact and dashboard visibility |
| CPU Stress | Increases CPU usage | Resource pressure and scaling behaviour |
| Memory Stress | Increases memory usage | Stability under memory pressure |

Each experiment will include an incident-style report:

```text
Hypothesis
Failure injected
Expected result
Actual result
Recovery time
Metrics observed
Lessons learned
Improvement made
```

---

## 📊 Observability Roadmap

The observability stack will be added after the Docker Compose and Kubernetes foundations are stable.

Planned tools:

| Tool | Purpose |
|---|---|
| Prometheus | Collect application and infrastructure metrics |
| Grafana | Display dashboards and recovery evidence |
| Kubernetes Metrics | Track pod status, restarts, CPU, and memory |
| Application Metrics | Track request count, error rate, and latency |

Planned dashboard panels:

```text
API uptime
Request rate
Error rate
Request latency
Pod restarts
CPU usage
Memory usage
Recovery time after failure
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
│   └── architecture-notes.md
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
| Version Control | Git, GitHub, commits, public repository |
| Documentation | README, roadmap, architecture notes |
| Backend Development | FastAPI service and endpoint design |
| API Testing | Pytest, FastAPI TestClient |
| CI | GitHub Actions automated tests |
| Containerisation | Dockerfile, Docker image build |
| Local Orchestration | Docker Compose |
| Troubleshooting | Python import paths, pytest configuration, container testing |
| Reliability Thinking | Health checks, readiness checks, failure planning |
| Future Platform Skills | Kubernetes, Prometheus, Grafana, chaos engineering |

---

## 🔮 Future Improvements

- Add PostgreSQL service to Docker Compose
- Add Redis service to Docker Compose
- Update `/ready` to check real dependency connections
- Add frontend status page
- Add Prometheus metrics endpoint
- Add Grafana dashboard package
- Add Kubernetes manifests
- Add liveness and readiness probes
- Add local Kubernetes deployment using Minikube or Kind
- Add LitmusChaos or Chaos Mesh experiments
- Add incident reports for each chaos experiment
- Add screenshots and demo evidence
- Add optional Azure AKS deployment
- Add optional Google Kubernetes Engine deployment
- Add security and dependency scanning
- Add release tags and GitHub project milestones

---

## 👤 Author

**Khairul Rizal**

DevOps and Cloud Support learner building practical cloud-native projects focused on reliability, resilience, observability, and automation.

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

Built as a DevOps and Cloud Support portfolio project.

Last updated: June 2026
