# Incident Report 02 — Kubernetes API Pod Failure Test

![Kubernetes](https://img.shields.io/badge/kubernetes-local%20kind-326CE5.svg)
![Status](https://img.shields.io/badge/test-passed-success.svg)
![Failure Type](https://img.shields.io/badge/failure-api%20pod%20deletion-orange.svg)
![Recovery](https://img.shields.io/badge/recovery-kubernetes%20recreated%20pod-blue.svg)

## Experiment Name

Kubernetes API Pod Failure Test

## Date

June 2026

## Environment

| Item | Value |
|---|---|
| Platform | Local Kubernetes |
| Cluster Tool | Kind |
| Namespace | `chaos-sandbox` |
| Application | `chaos-api` |
| API Image | `chaos-api:0.2.0` |
| Service Type | `ClusterIP` |
| Access Method | `kubectl port-forward` |

---

## Purpose

This experiment tested how the API service behaves when its Kubernetes pod is manually deleted.

The goal was to confirm that Kubernetes can detect that the desired application pod is missing and automatically create a replacement pod.

This is one of the core resilience benefits of Kubernetes: the system constantly tries to match the desired state declared in the Deployment manifest.

---

## Hypothesis

If the running API pod is deleted, the Kubernetes Deployment should automatically create a replacement pod.

Expected result:

```text
API pod deleted
 ↓
Kubernetes detects missing replica
 ↓
ReplicaSet creates a new pod
 ↓
New API pod becomes Running
 ↓
Deployment returns to 1/1 available
```

---

## System State Before Failure

The application was running inside the local Kind Kubernetes cluster.

Expected running components:

```text
chaos-api
chaos-postgres
chaos-redis
```

The API service was exposed locally using port-forwarding:

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

The API readiness endpoint was expected to show:

```text
status: ready
database: reachable
cache: reachable
```

---

## Failure Injected

The running API pod was manually deleted using Kubernetes.

Example command:

```bash
kubectl delete pod <API_POD_NAME> -n chaos-sandbox
```

This simulated an application pod failure.

In a real-world environment, this could represent:

- An application crash
- A container failure
- A node-level interruption
- A manual operational mistake
- A failed deployment causing a pod restart

---

## Expected Result

The API pod should temporarily disappear, but the Deployment should create a replacement pod.

Expected Kubernetes behavior:

```text
Old API pod terminates
New API pod is created
New API pod moves to Running
Readiness probe passes
Deployment becomes available again
```

---

## Actual Result

After the API pod was deleted, Kubernetes recreated the pod successfully.

Observed pod status:

```text
NAME                             READY   STATUS    RESTARTS   AGE
chaos-api-b8b88ddf9-2mtj4        1/1     Running   0          2m22s
chaos-postgres-5d4778d86-qpddz   1/1     Running   0          9m4s
chaos-redis-7cb6577fc6-l9wfc     1/1     Running   0          9m3s
```

Observed Deployment status:

```text
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
chaos-api   1/1     1            1           9m3s
```

The Deployment showed:

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

This confirms that the Deployment returned to the desired state.

---

## Kubernetes Deployment Details

The `chaos-api` Deployment was configured with one desired replica.

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

The API container used the following image:

```text
chaos-api:0.2.0
```

The Deployment also included both liveness and readiness probes.

### Liveness Probe

```text
http-get http://:8000/health
initial delay: 20s
timeout: 5s
period: 20s
failure threshold: 3
```

The liveness probe checks whether the API process is alive.

### Readiness Probe

```text
http-get http://:8000/ready
initial delay: 15s
timeout: 5s
period: 10s
failure threshold: 3
```

The readiness probe checks whether the API is ready to receive traffic, including whether its dependencies are reachable.

---

## Recovery Evidence

The Deployment condition showed that the new ReplicaSet was available.

```text
Conditions:
  Type           Status  Reason
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
```

The Deployment event showed that Kubernetes scaled the ReplicaSet to one pod.

```text
Events:
  Type    Reason             From                   Message
  Normal  ScalingReplicaSet  deployment-controller  Scaled up replica set chaos-api-b8b88ddf9 from 0 to 1
```

This confirms that Kubernetes handled the recovery automatically.

---

## Result Summary

| Check | Result |
|---|---|
| API pod failure injected | Yes |
| Kubernetes detected missing pod | Yes |
| Replacement API pod created | Yes |
| New pod reached Running state | Yes |
| Deployment returned to 1/1 available | Yes |
| PostgreSQL remained running | Yes |
| Redis remained running | Yes |
| Manual application restart required | No |
| Manual Kubernetes redeployment required | No |

---

## What This Proves

This test proves that Kubernetes manages desired state through Deployments and ReplicaSets.

The Deployment declared that one API replica should exist. When the running API pod was deleted, Kubernetes automatically created a new pod to restore the desired state.

This is different from running a single Docker container manually. With a standalone Docker container, if the container is deleted and no restart policy or orchestrator is managing it, it may not recover automatically.

With Kubernetes, the Deployment acts like a controller that continuously checks:

```text
What should be running?
What is actually running?
What needs to be fixed?
```

---

## Lessons Learned

This experiment showed why Kubernetes is useful for resilient systems.

Important lessons:

| Concept | Lesson |
|---|---|
| Deployment | Defines the desired number of running replicas |
| ReplicaSet | Creates replacement pods when needed |
| Pod | Temporary workload unit that can be replaced |
| Liveness Probe | Checks whether the application process is alive |
| Readiness Probe | Checks whether the application is ready for traffic |
| Desired State | Kubernetes continuously tries to match the declared configuration |

The API recovered because Kubernetes was responsible for managing it.

---

## Limitation of This Test

This test used only one API replica.

That means there may be brief downtime while the replacement pod is starting.

Current setup:

```text
API replicas: 1
```

A more resilient setup would use at least two replicas:

```text
API replicas: 2
```

With two replicas, one pod could fail while another pod continues serving traffic.

---

## Future Improvement

The next improvement should be to increase the API Deployment replica count from one to two.

Then the same pod deletion experiment should be repeated.

The follow-up test should compare:

| Test | Expected Behavior |
|---|---|
| 1 replica | Possible short interruption |
| 2 replicas | Service should remain more available |

Future improvements:

- Increase API replicas to 2
- Add request testing during pod deletion
- Measure recovery time more accurately
- Add Prometheus metrics
- Add Grafana dashboard evidence
- Add automated chaos testing using LitmusChaos or Chaos Mesh
- Compare pod failure impact before and after scaling

---

## Portfolio Value

This experiment demonstrates practical Kubernetes resilience knowledge.

It shows the ability to:

- Deploy an application to Kubernetes
- Use Deployments and Services
- Configure readiness and liveness probes
- Simulate pod failure
- Observe Kubernetes recovery
- Document results in an incident-style report
- Explain the difference between application health and application readiness

This is directly relevant to DevOps, Cloud Support, Platform Engineering, and Site Reliability Engineering roles.

---

## Final Result

The Kubernetes API pod failure test passed.

Kubernetes successfully recreated the deleted API pod and restored the Deployment to the desired state.

```text
Final result: PASS
```
