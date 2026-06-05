# Incident Report 03 — Kubernetes API Replica Resilience Improvement

![Kubernetes](https://img.shields.io/badge/kubernetes-local%20kind-326CE5.svg)
![Status](https://img.shields.io/badge/test-passed-success.svg)
![Improvement](https://img.shields.io/badge/improvement-api%20replicas%202-blue.svg)
![Recovery](https://img.shields.io/badge/recovery-higher%20availability-success.svg)

## Experiment Name

Kubernetes API Replica Resilience Improvement

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
| Previous Replica Count | `1` |
| Updated Replica Count | `2` |
| Service Type | `ClusterIP` |
| Access Method | `kubectl port-forward` |

---

## Purpose

This experiment improved the resilience of the API service by increasing the number of API replicas from one to two.

The earlier Kubernetes pod failure test proved that Kubernetes could recreate a deleted API pod. However, with only one API pod running, there could still be a brief service interruption while Kubernetes creates and starts the replacement pod.

This improvement tests a more resilient setup where two API pods run at the same time.

---

## Background

In the previous test, the API Deployment used one replica:

```yaml
replicas: 1
```

That setup proved Kubernetes recovery, but it had a limitation:

```text
If the only API pod fails, there may be a short period where no API pod is available.
```

To improve availability, the API Deployment was updated to use two replicas:

```yaml
replicas: 2
```

With two replicas, one pod can fail while another pod continues running.

---

## Hypothesis

If the API Deployment has two replicas and one API pod fails, Kubernetes should replace the failed pod while the other API pod remains running.

Expected result:

```text
2 API pods running
 ↓
1 API pod deleted
 ↓
1 API pod remains available
 ↓
Kubernetes creates a replacement pod
 ↓
Deployment returns to 2/2 available
```

---

## Change Made

The API Deployment manifest was updated.

File changed:

```text
k8s/api-deployment.yaml
```

Before:

```yaml
replicas: 1
```

After:

```yaml
replicas: 2
```

The updated manifest was applied with:

```bash
kubectl apply -f k8s/api-deployment.yaml
```

---

## System State After Scaling

After the Deployment was updated, Kubernetes created a second API pod.

Observed pod status:

```text
NAME                             READY   STATUS    RESTARTS   AGE
chaos-api-b8b88ddf9-2mtj4        1/1     Running   0          9m50s
chaos-api-b8b88ddf9-tvp6z        1/1     Running   0          92s
chaos-postgres-5d4778d86-qpddz   1/1     Running   0          16m
chaos-redis-7cb6577fc6-l9wfc     1/1     Running   0          16m
```

Observed Deployment status:

```text
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
chaos-api   2/2     2            2           16m
```

The Deployment details confirmed:

```text
Replicas: 2 desired | 2 updated | 2 total | 2 available | 0 unavailable
```

This confirms that the application now has two available API replicas.

---

## Kubernetes Deployment Details

The `chaos-api` Deployment now runs two replicas.

```text
Replicas: 2 desired | 2 updated | 2 total | 2 available | 0 unavailable
```

The active ReplicaSet is:

```text
chaos-api-b8b88ddf9
```

The ReplicaSet successfully created two API pods:

```text
NewReplicaSet: chaos-api-b8b88ddf9 (2/2 replicas created)
```

The Deployment condition showed that the application was available:

```text
Conditions:
  Type           Status  Reason
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
```

---

## Scaling Evidence

Kubernetes events showed that the Deployment was first created with one replica and later scaled to two replicas.

```text
Events:
  Type    Reason             From                   Message
  Normal  ScalingReplicaSet  deployment-controller  Scaled up replica set chaos-api-b8b88ddf9 from 0 to 1
  Normal  ScalingReplicaSet  deployment-controller  Scaled up replica set chaos-api-b8b88ddf9 from 1 to 2
```

This confirms that Kubernetes accepted the updated Deployment configuration and scaled the API service successfully.

---

## Health and Readiness Configuration

The API container still uses both liveness and readiness probes.

### Liveness Probe

```text
http-get http://:8000/health
initial delay: 20s
timeout: 5s
period: 20s
failure threshold: 3
```

The liveness probe confirms whether the API process is alive.

### Readiness Probe

```text
http-get http://:8000/ready
initial delay: 15s
timeout: 5s
period: 10s
failure threshold: 3
```

The readiness probe confirms whether the API is ready to receive traffic and whether its dependencies are reachable.

---

## Result Summary

| Check | Result |
|---|---|
| API replica count increased | Yes |
| Deployment applied successfully | Yes |
| Two API pods running | Yes |
| Deployment returned `2/2` ready | Yes |
| PostgreSQL remained running | Yes |
| Redis remained running | Yes |
| Liveness probe still configured | Yes |
| Readiness probe still configured | Yes |
| Kubernetes accepted desired state | Yes |

---

## Before and After Comparison

| Area | Before | After |
|---|---|---|
| API replicas | `1` | `2` |
| Available API pods | `1/1` | `2/2` |
| Failure tolerance | Lower | Higher |
| Risk during pod deletion | Possible short interruption | Reduced interruption risk |
| Kubernetes recovery | Recreate missing pod | Recreate missing pod while another stays running |
| Portfolio value | Shows recovery | Shows recovery plus resilience improvement |

---

## What This Proves

This improvement proves that Kubernetes can not only recover failed workloads, but also improve availability when multiple replicas are used.

The Deployment now declares that two API pods should always be running.

Kubernetes continuously checks the actual state against the desired state:

```text
Desired state: 2 API pods
Actual state: 2 API pods
Result: Deployment healthy
```

If one API pod fails, Kubernetes should restore the system back to two pods.

---

## Why Two Replicas Matter

Running two replicas is important because it reduces the risk of service interruption.

With one replica:

```text
1 API pod fails
 ↓
No API pod may be available until replacement starts
```

With two replicas:

```text
1 API pod fails
 ↓
1 API pod remains running
 ↓
Kubernetes creates replacement pod
```

This is a basic but important reliability pattern in Kubernetes.

---

## Lessons Learned

This experiment showed that resilience is not only about recovery after failure.

Resilience also includes reducing the impact of failure before it happens.

Important lessons:

| Concept | Lesson |
|---|---|
| Replicas | More replicas improve availability |
| Deployment | Controls the desired number of pods |
| ReplicaSet | Creates and maintains the required pod count |
| Readiness Probe | Helps ensure only ready pods receive traffic |
| Scaling | Kubernetes can increase pod count based on manifest changes |
| Resilience | Better design reduces the impact of failure |

---

## Limitation of This Improvement

This setup improves availability, but it does not make the system fully production-ready.

Current limitations:

- The API has two replicas, but PostgreSQL still has one pod.
- Redis still has one pod.
- No external load balancer is used yet.
- No ingress controller is configured yet.
- No Prometheus/Grafana monitoring is configured yet.
- No automated chaos engineering tool is installed yet.
- Recovery time is not measured automatically yet.

This is still a local learning environment, but it demonstrates an important resilience improvement.

---

## Future Improvements

Recommended next improvements:

- Repeat the API pod deletion test with two replicas.
- Measure whether the API stays reachable during pod deletion.
- Add a simple request loop to test availability during failure.
- Add Prometheus metrics.
- Add Grafana dashboards.
- Add Kubernetes metrics-server.
- Add LitmusChaos or Chaos Mesh for automated pod failure experiments.
- Add incident report screenshots from terminal and dashboard output.
- Add Redis and PostgreSQL failure tests in Kubernetes.

---

## Portfolio Value

This improvement strengthens the project because it shows the full engineering cycle:

```text
Deploy system
 ↓
Inject failure
 ↓
Observe recovery
 ↓
Identify weakness
 ↓
Improve design
 ↓
Validate improvement
 ↓
Document results
```

This is the type of thinking used in DevOps, Cloud Support, Platform Engineering, and Site Reliability Engineering.

It shows that the project is not only about creating YAML files. It is about using Kubernetes to design a more resilient system.

---

## Final Result

The Kubernetes API replica improvement passed.

The API Deployment was successfully scaled from one replica to two replicas.

Kubernetes confirmed the desired state:

```text
Replicas: 2 desired | 2 updated | 2 total | 2 available | 0 unavailable
```

```text
Final result: PASS
```
