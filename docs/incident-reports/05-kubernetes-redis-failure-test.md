# Incident Report 05 — Kubernetes Redis Failure Test

![Kubernetes](https://img.shields.io/badge/kubernetes-local%20kind-326CE5.svg)
![Status](https://img.shields.io/badge/test-passed-success.svg)
![Failure Type](https://img.shields.io/badge/failure-redis%20pod%20deletion-orange.svg)
![Recovery](https://img.shields.io/badge/recovery-kubernetes%20recreated%20redis%20pod-blue.svg)
![Readiness](https://img.shields.io/badge/readiness-no%20visible%20interruption-success.svg)

## Experiment Name

Kubernetes Redis Failure Test

## Date

June 2026

## Environment

| Item | Value |
|---|---|
| Platform | Local Kubernetes |
| Cluster Tool | Kind |
| Namespace | `chaos-sandbox` |
| API Application | `chaos-api` |
| Cache Dependency | `chaos-redis` |
| Redis Image | `redis:7-alpine` |
| API Replicas | `2` |
| Redis Replicas | `1` |
| Test Endpoint | `/ready` |
| Access Method | `kubectl port-forward` |

---

## Purpose

This experiment tested how the Kubernetes-based application behaves when the Redis cache pod is manually deleted.

Redis is used as a dependency for the API readiness check. The API checks Redis by sending a `PING` request through the `/ready` endpoint.

The goal of this experiment was to confirm whether:

- Kubernetes recreates the deleted Redis pod.
- The API remains alive during Redis failure.
- The `/ready` endpoint detects any visible Redis interruption.
- The system returns to a healthy state after Redis recovery.

---

## Hypothesis

If the Redis pod is deleted, Kubernetes should create a replacement Redis pod because Redis is managed by a Deployment.

Expected behavior:

```text
Redis pod deleted
 ↓
Kubernetes detects missing Redis replica
 ↓
ReplicaSet creates a replacement Redis pod
 ↓
Redis readiness probe passes
 ↓
API /ready returns ready again
```

Since Redis only has one replica, a brief readiness interruption may be possible.

Expected possible `/ready` behavior:

```text
Before failure: ready
During failure: not_ready, if Redis is unavailable long enough to be observed
After recovery: ready
```

---

## System State Before Failure

Before the failure test, all Kubernetes pods were running.

Expected components:

```text
chaos-api
chaos-postgres
chaos-redis
```

The API was running with two replicas:

```text
chaos-api   2/2 ready
```

Redis was running with one replica:

```text
chaos-redis   1/1 ready
```

The API readiness endpoint was expected to show:

```text
status: ready
database: reachable
cache: reachable
```

---

## Failure Injected

The Redis pod was manually deleted using Kubernetes.

Command used:

```bash
kubectl delete pod <REDIS_POD_NAME> -n chaos-sandbox
```

After deletion, Kubernetes created a replacement Redis pod.

Replacement pod observed:

```text
chaos-redis-7cb6577fc6-cln5s
```

---

## Readiness Observation Method

A loop was used to repeatedly check the API `/ready` endpoint while Redis was deleted and recreated.

Command used:

```bash
for i in {1..60}; do
  echo -n "Request $i: "
  curl -s http://127.0.0.1:8000/ready | grep -o '"status":"[^"]*"'
  sleep 1
done
```

The goal was to observe whether the API readiness status changed during Redis failure.

---

## Expected Result

A possible expected result was:

```text
"status":"ready"
"status":"not_ready"
"status":"ready"
```

This would indicate that the API briefly detected Redis as unavailable.

However, it was also possible that Redis would recover quickly enough that the readiness loop would not capture a visible interruption.

---

## Actual Result

The `/ready` loop stayed ready throughout the test.

Observed readiness behavior:

```text
/ready loop status: all ready
```

This means no visible readiness interruption was captured during the polling window.

After Redis was deleted, Kubernetes successfully recreated the Redis pod.

Observed pod status after recovery:

```text
NAME                             READY   STATUS    RESTARTS        AGE
chaos-api-b8b88ddf9-2mtj4        1/1     Running   1 (4m24s ago)   4d17h
chaos-api-b8b88ddf9-wxrwl        1/1     Running   1 (4m24s ago)   4d17h
chaos-postgres-5d4778d86-qpddz   1/1     Running   1 (4m24s ago)   4d17h
chaos-redis-7cb6577fc6-cln5s     1/1     Running   0               26s
```

Observed Redis Deployment status:

```text
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
chaos-redis   1/1     1            1           4d17h
```

Deployment details confirmed:

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

---

## Kubernetes Redis Deployment Details

The Redis Deployment is managed by Kubernetes.

Redis container image:

```text
redis:7-alpine
```

Redis exposes port:

```text
6379/TCP
```

The Redis Deployment includes both liveness and readiness probes.

### Liveness Probe

```text
exec [redis-cli ping]
delay: 10s
timeout: 1s
period: 20s
failure threshold: 3
```

The liveness probe checks whether Redis is still alive.

### Readiness Probe

```text
exec [redis-cli ping]
delay: 5s
timeout: 1s
period: 10s
failure threshold: 3
```

The readiness probe checks whether Redis is ready to receive traffic.

---

## Recovery Evidence

The Redis Deployment returned to the desired state.

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

The Redis Deployment condition showed:

```text
Conditions:
  Type           Status  Reason
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
```

The active ReplicaSet confirmed:

```text
NewReplicaSet: chaos-redis-7cb6577fc6 (1/1 replicas created)
```

This confirms that Kubernetes restored the Redis workload successfully.

---

## Result Summary

| Check | Result |
|---|---|
| Redis pod deleted manually | Yes |
| Kubernetes recreated Redis pod | Yes |
| New Redis pod reached `Running` | Yes |
| Redis Deployment returned to `1/1` available | Yes |
| API pods remained running | Yes |
| PostgreSQL remained running | Yes |
| `/ready` loop observed `not_ready` | No |
| `/ready` stayed ready throughout observed test | Yes |
| Manual Redis redeployment required | No |
| Test result | Pass |

---

## What This Proves

This experiment proves that Redis is being managed by Kubernetes through a Deployment.

When the Redis pod was deleted, Kubernetes recreated it automatically and restored the Redis Deployment to the desired state.

The API remained available during the observed test, and the `/ready` endpoint did not visibly change to `not_ready`.

This suggests that Redis recovered quickly enough that the one-second polling loop did not capture a readiness failure.

---

## Important Observation

The fact that `/ready` stayed ready does not necessarily mean Redis was never unavailable.

It means that no Redis interruption was captured by the readiness check loop.

Possible reasons:

- Redis restarted very quickly.
- The API request did not hit Redis during the brief unavailable window.
- Kubernetes recreated the Redis pod before the next readiness check detected failure.
- The polling interval of one second was not frequent enough to capture a very short outage.

This is still a valid result because the system recovered quickly and no visible API readiness impact was observed.

---

## Lessons Learned

| Concept | Lesson |
|---|---|
| Kubernetes Deployment | Restores deleted dependency pods automatically |
| Redis Dependency | Cache failures can be short-lived in a local Kubernetes test |
| Readiness Checks | Useful for detecting dependency health, but polling interval matters |
| Recovery Testing | Fast recovery may result in no visible failure from the client side |
| Observability | Prometheus and Grafana can help capture more detailed timing later |
| Experiment Design | Future tests should measure timing more precisely |

---

## Limitation of This Test

This test used a simple one-second readiness polling loop.

Limitations:

- The failure window may have been shorter than the polling interval.
- `/ready` only reports the result at the moment of each request.
- No Prometheus alert was configured yet.
- No Redis-specific dashboard panel was created yet.
- Redis only runs as a single pod without persistent storage.
- This was tested in a local Kind cluster, not a production Kubernetes environment.

---

## Future Improvements

Recommended next improvements:

- Repeat the Redis failure test with faster request polling.
- Use the reusable availability script against `/ready` during Redis deletion.
- Add Redis failure metrics to Grafana.
- Add Prometheus alerting for failed readiness checks.
- Add API-level metric for dependency status.
- Add a custom metric for Redis connectivity.
- Add Kubernetes event capture to the report.
- Add screenshots from Grafana during dependency failure.
- Repeat the same type of test for PostgreSQL.
- Compare Redis failure behavior with PostgreSQL failure behavior.

---

## Portfolio Value

This test adds value to the project because it shows dependency failure testing inside Kubernetes.

It demonstrates the ability to:

- Run a multi-service application in Kubernetes.
- Identify Redis as a dependency.
- Simulate a dependency pod failure.
- Observe API readiness behavior.
- Confirm Kubernetes recovery.
- Document results honestly, including when an expected failure was not visibly observed.

This is important because real DevOps and Cloud Support work often involves investigating dependencies, not just application containers.

---

## Final Result

The Kubernetes Redis failure test passed.

Redis was manually deleted, Kubernetes recreated the Redis pod, and the Redis Deployment returned to `1/1` available.

The API remained ready throughout the observed test.

```text
Final result: PASS
Readiness interruption observed: No
Redis recovery: Successful
```
