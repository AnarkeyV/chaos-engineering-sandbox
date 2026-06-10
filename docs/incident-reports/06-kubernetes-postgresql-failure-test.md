# Incident Report 06 — Kubernetes PostgreSQL Failure Test

![Kubernetes](https://img.shields.io/badge/kubernetes-local%20kind-326CE5.svg)
![Status](https://img.shields.io/badge/test-passed-success.svg)
![Failure Type](https://img.shields.io/badge/failure-postgresql%20pod%20deletion-orange.svg)
![Readiness](https://img.shields.io/badge/readiness-not__ready%20observed-red.svg)
![Recovery](https://img.shields.io/badge/recovery-kubernetes%20recreated%20postgresql%20pod-blue.svg)

## Experiment Name

Kubernetes PostgreSQL Failure Test

## Date

June 2026

## Environment

| Item | Value |
|---|---|
| Platform | Local Kubernetes |
| Cluster Tool | Kind |
| Namespace | `chaos-sandbox` |
| API Application | `chaos-api` |
| Database Dependency | `chaos-postgres` |
| PostgreSQL Image | `postgres:16-alpine` |
| API Replicas | `2` |
| PostgreSQL Replicas | `1` |
| Redis Replicas | `1` |
| Test Endpoint | `/ready` |
| Access Method | `kubectl port-forward` |

---

## Purpose

This experiment tested how the Kubernetes-based application behaves when the PostgreSQL database pod is manually deleted.

PostgreSQL is used as a dependency for the API readiness check. The API checks PostgreSQL by connecting to the database and running:

```sql
SELECT 1;
```

The goal of this experiment was to confirm whether:

- Kubernetes recreates the deleted PostgreSQL pod.
- The API process remains alive during database failure.
- The `/ready` endpoint detects PostgreSQL unavailability.
- The system returns to a ready state after PostgreSQL recovery.

---

## Hypothesis

If the PostgreSQL pod is deleted, Kubernetes should create a replacement PostgreSQL pod because PostgreSQL is managed by a Deployment.

Expected behavior:

```text
PostgreSQL pod deleted
 ↓
API /health should remain healthy
 ↓
API /ready should become not_ready
 ↓
Database dependency should show unreachable
 ↓
Kubernetes recreates PostgreSQL pod
 ↓
PostgreSQL readiness probe passes
 ↓
API /ready returns ready again
```

---

## System State Before Failure

Before the failure test, the API `/ready` endpoint returned ready.

Readiness result before failure:

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

This confirmed that both PostgreSQL and Redis were reachable before the failure was injected.

---

## Failure Injected

The PostgreSQL pod was manually deleted using Kubernetes.

Command used:

```bash
kubectl delete pod <POSTGRES_POD_NAME> -n chaos-sandbox
```

The PostgreSQL pod was recreated by Kubernetes.

Replacement pod observed:

```text
chaos-postgres-5d4778d86-mmfjl
```

---

## Readiness Observation Method

A loop was used to repeatedly check the API `/ready` endpoint while PostgreSQL was deleted and recreated.

Command used:

```bash
for i in {1..90}; do
  echo -n "Request $i: "
  curl -s http://127.0.0.1:8000/ready | grep -o '"status":"[^"]*"'
  sleep 1
done
```

This helped observe whether the API changed from `ready` to `not_ready` during the database failure.

---

## Expected Result

Expected `/ready` behavior:

```text
Before failure: ready
During PostgreSQL failure: not_ready
After PostgreSQL recovery: ready
```

Expected dependency behavior:

```text
database: unreachable
cache: reachable
```

This would indicate that the API correctly identified PostgreSQL failure while Redis remained healthy.

---

## Actual Readiness Result

The API readiness endpoint detected the PostgreSQL failure.

Observed output:

```text
Request 17: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 18: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 19: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 20: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 21: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 22: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 23: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 24: "status":"not_ready"
"status":"unreachable"
"status":"reachable"

Request 25: "status":"ready"
```

This shows that PostgreSQL was unreachable from requests 17 to 24.

Redis remained reachable during the same period.

The API returned to ready on request 25.

---

## Recovery Timing Observation

Based on the one-second readiness loop:

| Observation | Result |
|---|---|
| First visible `not_ready` request | Request 17 |
| Last visible `not_ready` request | Request 24 |
| First visible recovery request | Request 25 |
| Approximate visible readiness impact | Around 8 seconds |
| Database status during failure | `unreachable` |
| Redis status during failure | `reachable` |

This means the failure was clearly detected by the API readiness check.

---

## Kubernetes Pod Recovery Evidence

During pod recovery, Kubernetes showed the new PostgreSQL pod moving from not ready to ready.

Observed watch output:

```text
NAME                             READY   STATUS    RESTARTS      AGE
chaos-api-b8b88ddf9-2mtj4        1/1     Running   1 (16m ago)   4d17h
chaos-api-b8b88ddf9-wxrwl        1/1     Running   1 (16m ago)   4d17h
chaos-postgres-5d4778d86-mmfjl   0/1     Running   0             3s
chaos-redis-7cb6577fc6-cln5s     1/1     Running   0             12m

chaos-postgres-5d4778d86-mmfjl   1/1     Running   0             10s
```

This confirms that the PostgreSQL pod started first, then became ready after its readiness probe passed.

---

## Final Kubernetes State

After recovery, all pods were running and ready.

```text
NAME                             READY   STATUS    RESTARTS      AGE
chaos-api-b8b88ddf9-2mtj4        1/1     Running   1 (17m ago)   4d17h
chaos-api-b8b88ddf9-wxrwl        1/1     Running   1 (17m ago)   4d17h
chaos-postgres-5d4778d86-mmfjl   1/1     Running   0             71s
chaos-redis-7cb6577fc6-cln5s     1/1     Running   0             13m
```

PostgreSQL Deployment status:

```text
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
chaos-postgres   1/1     1            1           4d17h
```

Deployment details confirmed:

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

---

## Kubernetes PostgreSQL Deployment Details

The PostgreSQL Deployment is managed by Kubernetes.

PostgreSQL container image:

```text
postgres:16-alpine
```

PostgreSQL exposes port:

```text
5432/TCP
```

Environment variables:

```text
POSTGRES_DB:        chaosdb
POSTGRES_USER:      chaosuser
POSTGRES_PASSWORD:  chaospassword
```

The PostgreSQL Deployment includes both liveness and readiness probes.

### Liveness Probe

```text
exec [pg_isready -U chaosuser -d chaosdb]
delay: 20s
timeout: 1s
period: 20s
failure threshold: 3
```

The liveness probe checks whether PostgreSQL is alive.

### Readiness Probe

```text
exec [pg_isready -U chaosuser -d chaosdb]
delay: 10s
timeout: 1s
period: 10s
failure threshold: 3
```

The readiness probe checks whether PostgreSQL is ready to accept connections.

---

## Recovery Evidence

The PostgreSQL Deployment returned to the desired state.

```text
Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

The PostgreSQL Deployment condition showed:

```text
Conditions:
  Type           Status  Reason
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
```

The active ReplicaSet confirmed:

```text
NewReplicaSet: chaos-postgres-5d4778d86 (1/1 replicas created)
```

This confirms that Kubernetes restored the PostgreSQL workload successfully.

---

## Result Summary

| Check | Result |
|---|---|
| PostgreSQL pod deleted manually | Yes |
| API stayed running | Yes |
| Redis stayed running | Yes |
| `/ready` detected PostgreSQL failure | Yes |
| `/ready` changed to `not_ready` | Yes |
| Database showed `unreachable` | Yes |
| Cache stayed `reachable` | Yes |
| Kubernetes recreated PostgreSQL pod | Yes |
| PostgreSQL pod reached `1/1 Running` | Yes |
| PostgreSQL Deployment returned to `1/1` available | Yes |
| API `/ready` returned to `ready` | Yes |
| Manual PostgreSQL redeployment required | No |
| Test result | Pass |

---

## What This Proves

This experiment proves that the API readiness check correctly detects PostgreSQL dependency failure.

The API itself did not crash, but it correctly reported that the overall service was not ready because the database dependency was unavailable.

This is an important difference:

```text
/health = Is the API process alive?
/ready  = Is the API ready to serve traffic with its dependencies?
```

During the test:

```text
API process: alive
PostgreSQL dependency: unavailable
Redis dependency: available
Overall readiness: not_ready
```

After PostgreSQL recovered, the API returned to ready.

---

## Why This Matters

In production systems, an application process can still be running even when a critical dependency is unavailable.

Without readiness checks, a platform might continue sending traffic to a service that cannot properly handle requests.

This test demonstrates why dependency-aware readiness checks are important.

It also shows that Kubernetes can restore a failed dependency pod, while the application can report degraded readiness during the failure window.

---

## Comparison with Redis Failure Test

The previous Redis failure test did not show a visible readiness interruption during one-second polling.

The PostgreSQL failure test behaved differently.

| Dependency | Failure Result |
|---|---|
| Redis | No visible readiness interruption captured |
| PostgreSQL | Clear `not_ready` state observed |
| Redis recovery | Very fast during observed test |
| PostgreSQL recovery | Visible readiness impact around 8 seconds |

This comparison shows that different dependencies can have different recovery characteristics.

---

## Lessons Learned

| Concept | Lesson |
|---|---|
| Dependency readiness | `/ready` should check critical dependencies |
| PostgreSQL failure | Database failure can visibly affect application readiness |
| Kubernetes recovery | Deployments recreate deleted pods automatically |
| Health vs readiness | A live API is not always ready to serve traffic |
| Redis vs PostgreSQL | Dependencies recover at different speeds |
| Experiment evidence | Request loops help capture short failure windows |
| Cloud Support thinking | Identifying which dependency failed is critical during incidents |

---

## Limitation of This Test

This test was run in a local Kind cluster.

Limitations:

- PostgreSQL had only one replica.
- No persistent volume was configured for PostgreSQL.
- No production-grade PostgreSQL high availability was used.
- The test used a simple one-second readiness loop.
- No automated Prometheus alert was configured yet.
- No database-specific Grafana dashboard panel was configured yet.
- This was not a managed cloud Kubernetes environment.

Despite these limitations, the test clearly demonstrated application dependency failure detection and Kubernetes recovery.

---

## Future Improvements

Recommended next improvements:

- Add a custom API metric for dependency readiness.
- Add Prometheus alerting for `not_ready` responses.
- Add Grafana panels for readiness failure count.
- Add PostgreSQL-specific metrics later.
- Add persistent storage for PostgreSQL.
- Add a PostgreSQL StatefulSet version for a more realistic database setup.
- Add MTTR calculation for dependency recovery.
- Add screenshots from Grafana during failure.
- Compare results between Redis and PostgreSQL failures.
- Add automated chaos experiments using LitmusChaos or Chaos Mesh.

---

## Portfolio Value

This test adds strong value to the project because it shows realistic dependency failure behavior.

It demonstrates the ability to:

- Run a multi-service application in Kubernetes.
- Identify PostgreSQL as a critical dependency.
- Simulate database pod failure.
- Observe readiness degradation.
- Confirm Redis stayed healthy during database failure.
- Confirm Kubernetes recreated the PostgreSQL pod.
- Document the difference between health and readiness.

This is directly relevant to DevOps, Cloud Support, Platform Engineering, and Site Reliability Engineering work.

---

## Final Result

The Kubernetes PostgreSQL failure test passed.

PostgreSQL was manually deleted, the API detected the database failure, `/ready` changed to `not_ready`, Kubernetes recreated the PostgreSQL pod, and the API returned to `ready`.

```text
Final result: PASS
Readiness interruption observed: Yes
Database failure detected: Yes
Redis remained reachable: Yes
PostgreSQL recovery: Successful
```
