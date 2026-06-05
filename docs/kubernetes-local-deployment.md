# ☸️ Kubernetes Local Deployment Guide

## Chaos Engineering Sandbox

This guide explains how to deploy the Chaos Engineering Sandbox application into a local Kubernetes cluster using **Kind**.

The goal is to move the project from Docker Compose into Kubernetes so that it can later support realistic chaos engineering experiments such as pod failure, dependency failure, recovery testing, and observability.

---

## 📋 Table of Contents

- [Purpose of This Guide](#purpose-of-this-guide)
- [What We Are Deploying](#what-we-are-deploying)
- [Why Kubernetes Matters](#why-kubernetes-matters)
- [What Kind Is](#what-kind-is)
- [Prerequisites](#prerequisites)
- [Kubernetes Files Created](#kubernetes-files-created)
- [Step 1: Check kubectl](#step-1-check-kubectl)
- [Step 2: Check Kind](#step-2-check-kind)
- [Step 3: Create the Kind Cluster](#step-3-create-the-kind-cluster)
- [Step 4: Build the API Docker Image](#step-4-build-the-api-docker-image)
- [Step 5: Load the Image into Kind](#step-5-load-the-image-into-kind)
- [Step 6: Apply the Kubernetes Manifests](#step-6-apply-the-kubernetes-manifests)
- [Step 7: Check Pods and Services](#step-7-check-pods-and-services)
- [Step 8: Test the API with Port Forwarding](#step-8-test-the-api-with-port-forwarding)
- [Useful Troubleshooting Commands](#useful-troubleshooting-commands)
- [How This Supports Chaos Engineering](#how-this-supports-chaos-engineering)
- [Clean Up Commands](#clean-up-commands)
- [Summary](#summary)

---

## Purpose of This Guide

This document explains how the project was deployed into a local Kubernetes environment.

At this stage, the application includes:

| Component | Purpose |
|---|---|
| FastAPI API | Main backend service |
| PostgreSQL | Database dependency |
| Redis | Cache dependency |
| Kubernetes | Runs and manages the containers |
| Kind | Provides a local Kubernetes cluster using Docker |

The project previously ran using Docker Compose.

Docker Compose is useful for local multi-container development, but Kubernetes is closer to how many production cloud-native systems are deployed.

Moving to Kubernetes allows the project to demonstrate:

- Deployments
- Services
- Namespaces
- Pods
- Liveness probes
- Readiness probes
- Service discovery
- Controlled failure testing
- Recovery behavior

---

## What We Are Deploying

The local Kubernetes deployment contains three main services:

```text
chaos-sandbox namespace
│
├── chaos-api
│   ├── FastAPI backend
│   ├── /health endpoint
│   ├── /ready endpoint
│   └── /status endpoint
│
├── chaos-postgres
│   └── PostgreSQL database dependency
│
└── chaos-redis
    └── Redis cache dependency
```

The expected service flow is:

```text
User / Browser
 ↓
kubectl port-forward
 ↓
chaos-api-service
 ↓
chaos-api pod
 ↓
PostgreSQL and Redis services
```

---

## Why Kubernetes Matters

Kubernetes is used to run and manage containerized applications.

In this project, Kubernetes helps demonstrate how cloud-native systems behave when something fails.

For example:

| Failure | Kubernetes Behavior to Observe |
|---|---|
| API pod crashes | Kubernetes can restart or recreate the pod |
| Redis becomes unavailable | API readiness can change to `not_ready` |
| PostgreSQL becomes unavailable | API can detect the database dependency failure |
| Application is unhealthy | Liveness probes can restart the container |
| Application is not ready | Readiness probes can stop traffic from being sent |

This is important for DevOps, Cloud Support, and SRE-style learning because real systems are expected to recover from failure, not just run when everything is perfect.

---

## What Kind Is

**Kind** stands for **Kubernetes in Docker**.

It allows a local Kubernetes cluster to run inside Docker containers.

This is useful because it allows Kubernetes learning and testing without needing a paid cloud cluster.

For this project, Kind is used to:

- Run Kubernetes locally
- Deploy the API, PostgreSQL, and Redis
- Test Kubernetes manifests
- Prepare for future chaos engineering experiments
- Avoid cloud costs during early development

---

## Prerequisites

Before following this guide, the following tools should be installed:

| Tool | Purpose |
|---|---|
| Docker Desktop | Runs containers and supports Kind |
| kubectl | Command-line tool for Kubernetes |
| Kind | Creates local Kubernetes clusters |
| Git | Version control |
| VS Code | Code editing |

Check Docker is running before creating the Kind cluster.

---

## Kubernetes Files Created

The Kubernetes manifests are stored in:

```text
k8s/
├── namespace.yaml
├── api-deployment.yaml
├── api-service.yaml
├── postgres-deployment.yaml
├── postgres-service.yaml
├── redis-deployment.yaml
└── redis-service.yaml
```

### File purpose

| File | Purpose |
|---|---|
| `namespace.yaml` | Creates a separate Kubernetes namespace for the project |
| `api-deployment.yaml` | Deploys the FastAPI application |
| `api-service.yaml` | Exposes the API inside the cluster |
| `postgres-deployment.yaml` | Deploys PostgreSQL |
| `postgres-service.yaml` | Exposes PostgreSQL inside the cluster |
| `redis-deployment.yaml` | Deploys Redis |
| `redis-service.yaml` | Exposes Redis inside the cluster |

---

## Step 1: Check kubectl

Run:

```bash
kubectl version --client
```

Expected result:

```text
Client Version: ...
```

If this command works, `kubectl` is installed correctly.

---

## Step 2: Check Kind

Run:

```bash
kind version
```

Expected result:

```text
kind v...
```

If Kind is not installed, install it with Homebrew:

```bash
brew install kind
```

---

## Step 3: Create the Kind Cluster

Create a local Kubernetes cluster named `chaos-sandbox`:

```bash
kind create cluster --name chaos-sandbox
```

Check cluster information:

```bash
kubectl cluster-info --context kind-chaos-sandbox
```

Check nodes:

```bash
kubectl get nodes
```

Expected result:

```text
NAME                          STATUS   ROLES           AGE   VERSION
chaos-sandbox-control-plane   Ready    control-plane   ...   ...
```

The important part is:

```text
STATUS = Ready
```

This means the local Kubernetes node is ready to run workloads.

---

## Step 4: Build the API Docker Image

From the project root, build the API image:

```bash
docker build -t chaos-api:0.2.0 -f app/api/Dockerfile .
```

This creates a local Docker image named:

```text
chaos-api:0.2.0
```

The Kubernetes API deployment uses this image name.

---

## Step 5: Load the Image into Kind

Kind does not automatically use every local Docker image from your machine.

The image must be loaded into the Kind cluster:

```bash
kind load docker-image chaos-api:0.2.0 --name chaos-sandbox
```

This makes the image available inside the local Kubernetes cluster.

Without this step, the API pod may fail with an image pull error.

---

## Step 6: Apply the Kubernetes Manifests

Apply the namespace first:

```bash
kubectl apply -f k8s/namespace.yaml
```

Then apply PostgreSQL:

```bash
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

Then apply Redis:

```bash
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml
```

Then apply the API:

```bash
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
```

These commands create all required Kubernetes resources.

---

## Step 7: Check Pods and Services

Check pods:

```bash
kubectl get pods -n chaos-sandbox
```

Expected result:

```text
NAME                              READY   STATUS    RESTARTS   AGE
chaos-api-xxxxx                   1/1     Running   0          ...
chaos-postgres-xxxxx              1/1     Running   0          ...
chaos-redis-xxxxx                 1/1     Running   0          ...
```

Check services:

```bash
kubectl get svc -n chaos-sandbox
```

Expected services:

```text
chaos-api-service
postgres
redis
```

The services allow pods to communicate with each other inside the cluster.

For example, the API connects to PostgreSQL using this hostname:

```text
postgres
```

And connects to Redis using this hostname:

```text
redis
```

---

## Step 8: Test the API with Port Forwarding

The API service is currently a `ClusterIP` service.

That means it is reachable inside the Kubernetes cluster, but not directly from the browser.

To access it locally, use port forwarding:

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

Then open these URLs in a browser:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/ready
http://127.0.0.1:8000/status
http://127.0.0.1:8000/docs
```

Expected `/health` result:

```json
{
  "status": "healthy",
  "service": "chaos-api"
}
```

Expected `/ready` result:

```json
{
  "status": "ready",
  "service": "chaos-api",
  "dependencies": {
    "database": {
      "status": "reachable"
    },
    "cache": {
      "status": "reachable"
    }
  }
}
```

Expected `/status` result:

```json
{
  "service": "chaos-api",
  "version": "0.2.0",
  "environment": "kubernetes-local",
  "features": {
    "database": true,
    "cache": true,
    "observability": false,
    "chaos_experiments": false
  }
}
```

---

## Useful Troubleshooting Commands

### Check all pods

```bash
kubectl get pods -n chaos-sandbox
```

### Check all services

```bash
kubectl get svc -n chaos-sandbox
```

### Describe a pod

```bash
kubectl describe pod <pod-name> -n chaos-sandbox
```

Example:

```bash
kubectl describe pod chaos-api-xxxxx -n chaos-sandbox
```

### View API logs

```bash
kubectl logs deployment/chaos-api -n chaos-sandbox
```

### View PostgreSQL logs

```bash
kubectl logs deployment/chaos-postgres -n chaos-sandbox
```

### View Redis logs

```bash
kubectl logs deployment/chaos-redis -n chaos-sandbox
```

### Restart the API deployment

```bash
kubectl rollout restart deployment/chaos-api -n chaos-sandbox
```

### Check rollout status

```bash
kubectl rollout status deployment/chaos-api -n chaos-sandbox
```

### Delete and reapply resources

```bash
kubectl delete -f k8s/ -n chaos-sandbox
kubectl apply -f k8s/
```

If namespace deletion is included, reapply the namespace first.

---

## Common Issues

### Issue 1: API pod shows ImagePullBackOff

Possible cause:

```text
The Docker image was not loaded into Kind.
```

Fix:

```bash
docker build -t chaos-api:0.2.0 -f app/api/Dockerfile .
kind load docker-image chaos-api:0.2.0 --name chaos-sandbox
kubectl rollout restart deployment/chaos-api -n chaos-sandbox
```

---

### Issue 2: API pod is running but not ready

Check readiness:

```bash
kubectl describe pod <api-pod-name> -n chaos-sandbox
```

Possible causes:

- PostgreSQL is not ready
- Redis is not ready
- Wrong environment variables
- API cannot connect to dependencies

Check logs:

```bash
kubectl logs deployment/chaos-api -n chaos-sandbox
```

---

### Issue 3: Browser cannot access the API

The service is `ClusterIP`, so it is not exposed publicly.

Use port forwarding:

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

Then open:

```text
http://127.0.0.1:8000/health
```

---

### Issue 4: Port 8000 is already in use

Use another local port:

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8001:8000
```

Then open:

```text
http://127.0.0.1:8001/health
```

---

## How This Supports Chaos Engineering

This Kubernetes deployment prepares the project for real chaos engineering experiments.

Instead of only stopping Docker containers manually, we can now test Kubernetes-level failures.

Future experiments can include:

| Experiment | What It Tests |
|---|---|
| Delete API pod | Can Kubernetes recreate the API pod? |
| Delete Redis pod | Can the API detect cache failure and recovery? |
| Delete PostgreSQL pod | Can the API detect database failure and recovery? |
| Scale API replicas | Does the service remain available during pod failure? |
| Add resource limits | How does the system behave under CPU or memory pressure? |
| Add network latency | How does latency affect readiness and response time? |

This is the foundation for future tools such as:

```text
LitmusChaos
Chaos Mesh
Prometheus
Grafana
```

---

## Clean Up Commands

### Delete Kubernetes resources only

```bash
kubectl delete -f k8s/api-service.yaml
kubectl delete -f k8s/api-deployment.yaml
kubectl delete -f k8s/redis-service.yaml
kubectl delete -f k8s/redis-deployment.yaml
kubectl delete -f k8s/postgres-service.yaml
kubectl delete -f k8s/postgres-deployment.yaml
kubectl delete -f k8s/namespace.yaml
```

### Delete the entire Kind cluster

```bash
kind delete cluster --name chaos-sandbox
```

Use this only if you want to completely remove the local Kubernetes cluster.

---

## Verification Checklist

The Kubernetes deployment is considered successful when:

```text
[ ] Kind cluster exists
[ ] Kubernetes node is Ready
[ ] chaos-api image is loaded into Kind
[ ] chaos-sandbox namespace exists
[ ] API pod is Running
[ ] PostgreSQL pod is Running
[ ] Redis pod is Running
[ ] Services exist for API, PostgreSQL, and Redis
[ ] Port forwarding works
[ ] /health returns healthy
[ ] /ready returns ready
[ ] /status shows database and cache as true
```

---

## Summary

This milestone moved the Chaos Engineering Sandbox from Docker Compose into Kubernetes.

The project now demonstrates:

- Local Kubernetes deployment using Kind
- Kubernetes namespace usage
- API, PostgreSQL, and Redis deployments
- Internal service discovery
- Liveness and readiness probes
- Local testing with port forwarding
- Preparation for Kubernetes-based chaos engineering experiments

This is a major step toward making the project a realistic DevOps, Cloud Support, and reliability engineering portfolio project.
