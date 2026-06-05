# Chaos Engineering Sandbox

A hands-on DevOps and Cloud Support portfolio project focused on building, monitoring, breaking, and improving a cloud-native system.

## Project Overview

The Chaos Engineering Sandbox is a learning and portfolio project designed to demonstrate how modern systems can be tested for resilience. Instead of only deploying a working application, this project intentionally introduces controlled failures into a microservices environment and observes how the system responds.

The goal is to build practical skills in:

- Docker
- Kubernetes
- CI/CD
- Observability
- Prometheus
- Grafana
- Chaos Engineering
- Incident Response
- Recovery Analysis
- Cloud-Native Reliability

## Why I Built This

I created this project to deepen my understanding of DevOps, Cloud Support, and reliability engineering. In real-world systems, failure is unavoidable. Services may crash, networks may slow down, containers may restart, and dependencies may become unavailable.

This sandbox allows me to safely test those situations, measure the impact, and document how the system recovers.

## Planned Architecture

The first version of the project will include:

- A backend API service
- A simple frontend service
- A PostgreSQL database
- A Redis cache
- Docker for containerization
- Kubernetes for orchestration
- Prometheus for metrics collection
- Grafana for dashboards
- LitmusChaos or Chaos Mesh for failure injection

## Roadmap

### Milestone 1: Repository Setup

- Create project structure
- Add README documentation
- Add GitHub repository
- Prepare folders for app, Kubernetes, observability, and chaos experiments

### Milestone 2: Backend Health API

- Build a simple FastAPI backend
- Add health check endpoints
- Prepare the service for Docker

### Milestone 3: Docker and Docker Compose

- Containerize the backend
- Add frontend service
- Add Redis and PostgreSQL
- Run the system locally

### Milestone 4: Kubernetes Deployment

- Create Kubernetes manifests
- Deploy services into a local Kubernetes cluster
- Add liveness and readiness probes

### Milestone 5: Observability

- Add Prometheus
- Add Grafana
- Create dashboards for uptime, errors, latency, and recovery

### Milestone 6: Chaos Experiments

- Run pod failure tests
- Run latency tests
- Run dependency failure tests
- Measure recovery time

### Milestone 7: Case Study and Portfolio Report

- Document each experiment
- Capture screenshots
- Explain what failed, what recovered, and what was improved

## Target Skills Demonstrated

This project is designed to demonstrate practical skills relevant to:

- DevOps Engineer roles
- Cloud Support Engineer roles
- Site Reliability Engineering roles
- Platform Engineering roles
- Infrastructure and operations roles

## Current Status

Project initialized. Milestone 1 in progress.

## Author

Khairul Rizal