# Architecture Notes

## Project Name

Chaos Engineering Sandbox

## Purpose of This Document

This document explains the planned architecture for the Chaos Engineering Sandbox project.

The goal is to keep the system simple enough for learning, but realistic enough to demonstrate DevOps, Cloud Support, Kubernetes, observability, and chaos engineering concepts.

This project is not only about deploying an application. It is about understanding what happens when parts of the system fail and how the system can recover.

---

## High-Level Architecture

The first version of the project will use a simple microservices-style architecture.

```text
User
 ↓
Frontend Service
 ↓
Backend API Service
 ↓
PostgreSQL Database

Backend API Service
 ↓
Redis Cache
```

In plain English:

1. The user opens the frontend.
2. The frontend talks to the backend API.
3. The backend API stores or retrieves data from PostgreSQL.
4. The backend API can also use Redis as a cache.
5. Monitoring tools observe the system.
6. Chaos engineering tools intentionally create controlled failures.
7. The system response is measured and documented.

---

## Main Components

### 1. Frontend Service

The frontend service will provide a simple web page or status dashboard for the user.

Its purpose is to show that the application is running and later display basic information from the backend API.

In the first version, this can be a simple HTML page. Later, it can be improved using a frontend framework if needed.

---

### 2. Backend API Service

The backend API will be the main application service.

It will be built using Python and FastAPI.

The API will expose health check and status endpoints that help us understand whether the service is working correctly.

Planned endpoints:

```text
GET /health
GET /ready
GET /status
GET /simulate-work
```

### Endpoint Purpose

| Endpoint | Purpose |
|---|---|
| `/health` | Confirms that the API container is alive |
| `/ready` | Confirms that the API is ready to receive traffic |
| `/status` | Shows the status of connected services such as PostgreSQL and Redis |
| `/simulate-work` | Simulates application activity for testing and monitoring |

---

### 3. PostgreSQL Database

PostgreSQL will be used as the database service.

Its purpose is to simulate a real application dependency.

Many real-world applications depend on databases. If the database becomes slow or unavailable, the application may also be affected.

This makes PostgreSQL useful for future chaos experiments such as:

- Database pod failure
- Database connection failure
- Slow database response
- Recovery testing

---

### 4. Redis Cache

Redis will be used as a cache service.

Its purpose is to simulate a fast temporary data dependency.

In real-world systems, Redis is often used to make applications faster by storing frequently used data in memory.

Redis is useful for chaos testing because we can observe what happens when the cache is unavailable.

Possible future experiments include:

- Redis pod failure
- Redis connection failure
- Cache unavailable scenario
- Graceful fallback testing

---

### 5. Docker

Docker will be used to package the application services into containers.

Each major part of the system will run in its own container.

Planned containers:

```text
Frontend container
Backend API container
PostgreSQL container
Redis container
```

Docker helps make the project easier to run consistently across different machines.

---

### 6. Docker Compose

Docker Compose will be used during the early local development stage.

It allows multiple containers to run together using one command.

For example:

```bash
docker compose up --build
```

This will be useful before moving the project into Kubernetes.

---

### 7. Kubernetes

Kubernetes will be used after the Docker Compose version is working.

Kubernetes will manage the containers as pods and services.

Planned Kubernetes resources:

```text
Namespace
Deployments
Services
ConfigMaps
Secrets
Persistent Volumes
Liveness Probes
Readiness Probes
```

Kubernetes is important for this project because it allows us to test recovery behavior.

For example, if a pod crashes, Kubernetes can restart or recreate it.

This is useful for chaos engineering because we can intentionally break something and observe how Kubernetes responds.

---

### 8. Prometheus

Prometheus will be used to collect metrics.

Metrics are numerical measurements that help us understand how the system is behaving.

Examples of useful metrics:

```text
Application uptime
Request count
Error rate
Request latency
CPU usage
Memory usage
Pod restarts
```

Prometheus helps us collect evidence during chaos experiments.

---

### 9. Grafana

Grafana will be used to create dashboards from Prometheus metrics.

Grafana will help us visually understand what happened before, during, and after a failure.

Possible dashboard panels:

```text
API availability
Request latency
Error rate
Pod restart count
CPU usage
Memory usage
Recovery time
```

Screenshots from Grafana will be added to the project documentation later.

---

### 10. Chaos Engineering Tool

A chaos engineering tool will be used to inject controlled failures into the system.

Possible tools:

```text
LitmusChaos
Chaos Mesh
```

For the first version, LitmusChaos is the preferred choice because it is commonly used with Kubernetes and is easier to explain in a portfolio project.

Possible experiments:

```text
API pod kill
Redis pod kill
Database pod kill
Network latency
CPU stress
Memory stress
```

The goal is not to break the system randomly.

The goal is to test specific failure scenarios safely and document the result.

---

## First Target Architecture

The first target architecture will run locally using Docker.

```text
Local Machine
│
├── Docker
│   ├── Frontend Container
│   ├── Backend API Container
│   ├── PostgreSQL Container
│   └── Redis Container
│
└── Local Development Tools
    ├── VS Code
    ├── Git
    └── GitHub
```

This allows the project to start simple before adding Kubernetes.

---

## Later Kubernetes Architecture

After the Docker version works, the system will move into Kubernetes.

```text
Local Kubernetes Cluster
│
├── Application Namespace
│   ├── Frontend Pod
│   ├── Backend API Pod
│   ├── PostgreSQL Pod
│   └── Redis Pod
│
├── Observability Namespace
│   ├── Prometheus
│   └── Grafana
│
└── Chaos Engineering Namespace
    └── LitmusChaos or Chaos Mesh
```

This structure separates the application, monitoring tools, and chaos tools into different areas.

This makes the project cleaner and easier to understand.

---

## Expected Traffic Flow

Normal application flow:

```text
User
 ↓
Frontend
 ↓
Backend API
 ↓
PostgreSQL
```

Cache flow:

```text
Backend API
 ↓
Redis
```

Monitoring flow:

```text
Prometheus
 ↓
Collects metrics from application and Kubernetes
 ↓
Grafana displays dashboards
```

Chaos experiment flow:

```text
Chaos Tool
 ↓
Injects controlled failure
 ↓
Application reacts
 ↓
Prometheus records metrics
 ↓
Grafana shows impact
 ↓
Documentation records result
```

---

## Failure Scenarios to Test

The project will eventually test several common failure scenarios.

### Scenario 1: API Pod Failure

The API pod is intentionally deleted or killed.

Expected result:

```text
Kubernetes recreates the pod.
The service recovers.
Recovery time is measured.
```

---

### Scenario 2: Redis Failure

The Redis service becomes unavailable.

Expected result:

```text
The API should continue working where possible.
The application should show degraded behavior instead of complete failure.
```

---

### Scenario 3: Database Failure

The database becomes unavailable.

Expected result:

```text
The API should detect the issue.
The error should be visible in logs and metrics.
The recovery process should be documented.
```

---

### Scenario 4: Network Latency

Artificial delay is introduced between services.

Expected result:

```text
Request latency increases.
Grafana shows slower response times.
The system impact is measured.
```

---

### Scenario 5: CPU or Memory Stress

A service is placed under resource pressure.

Expected result:

```text
CPU or memory usage increases.
Performance may degrade.
Kubernetes behavior is observed.
```

---

## Resilience Concepts Demonstrated

This project is designed to demonstrate the following DevOps and Cloud Support concepts:

```text
Containerization
Microservices
Kubernetes orchestration
Health checks
Liveness probes
Readiness probes
Monitoring
Observability
Failure injection
Incident response
Recovery time
MTTR
Service reliability
Graceful degradation
```

---

## Design Principles

### 1. Start Simple

The first version should be easy to run and understand.

The goal is not to create a complex application immediately.

The goal is to build the foundation properly.

---

### 2. Make Failure Visible

Every failure should be measurable.

If something breaks, the project should show:

```text
What failed
When it failed
How users were affected
How long recovery took
What was improved
```

---

### 3. Document Everything

The documentation is as important as the code.

A good portfolio project should explain the thinking behind the technical decisions.

Each experiment should include:

```text
Hypothesis
Failure injected
Expected result
Actual result
Recovery time
Lessons learned
Improvement made
```

---

### 4. Build Like a Real DevOps Project

The repository should be structured like a real-world engineering project.

That means it should include:

```text
Clear README
Architecture notes
Setup guide
Kubernetes manifests
Monitoring configuration
Chaos experiment files
Incident reports
Screenshots
CI/CD workflow
```

---

## Planned Folder Structure

```text
chaos-engineering-sandbox/
├── README.md
├── LICENSE
├── .gitignore
├── app/
│   ├── api/
│   └── frontend/
├── docs/
│   ├── project-roadmap.md
│   ├── architecture-notes.md
│   ├── setup-guide.md
│   ├── observability-guide.md
│   ├── chaos-experiments.md
│   └── incident-reports/
├── k8s/
├── observability/
├── chaos/
├── scripts/
└── .github/
    └── workflows/
```

---

## Final Architecture Goal

The final version of the project should demonstrate a complete DevOps reliability workflow:

```text
Build application
 ↓
Containerize application
 ↓
Deploy to Kubernetes
 ↓
Monitor with Prometheus and Grafana
 ↓
Inject controlled failures
 ↓
Observe impact
 ↓
Measure recovery
 ↓
Improve the system
 ↓
Document the results
```

---

## Summary

The Chaos Engineering Sandbox will be built as a practical learning project and portfolio showcase.

It will show how a cloud-native system can be deployed, monitored, intentionally broken, recovered, and improved.

The most important goal is not just to prove that the application works.

The most important goal is to prove that the system can handle failure and that the engineer understands what happened during that failure.
