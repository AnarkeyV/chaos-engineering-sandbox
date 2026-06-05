# Incident Report 04 — Two-Replica API Availability Test

![Kubernetes](https://img.shields.io/badge/kubernetes-local%20kind-326CE5.svg)
![Status](https://img.shields.io/badge/test-passed-success.svg)
![Availability](https://img.shields.io/badge/availability-60%2F60%20requests%20200-success.svg)
![Replicas](https://img.shields.io/badge/api%20replicas-2-blue.svg)

## Experiment Name

Two-Replica API Availability Test

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
| API Replicas | `2` |
| Service Type | `ClusterIP` |
| Access Method | `kubectl port-forward` |
| Test Endpoint | `/health` |
| Request Count | `60` |
| Request Frequency | 1 request per second |

---

## Purpose

This experiment tested whether the API remained available while one of two running API pods was deleted.

The previous experiments showed that Kubernetes could recreate a deleted pod and that the API Deployment could be improved from one replica to two replicas.

This test goes one step further.

Instead of only checking whether Kubernetes recreated the pod, this test continuously sent requests to the API while one pod was deleted.

The goal was to check whether users would still receive successful responses during the failure.

---

## Hypothesis

If the API Deployment has two replicas and one API pod is deleted, the Kubernetes Service should continue routing traffic to the remaining healthy API pod.

Expected result:

```text
2 API pods running
 ↓
Continuous requests sent to API service
 ↓
1 API pod deleted
 ↓
1 API pod remains available
 ↓
Kubernetes creates replacement pod
 ↓
Requests continue returning HTTP 200
 ↓
Deployment returns to 2/2 available
```

---

## System State Before Failure

The API Deployment was already scaled to two replicas.

Expected Deployment state:

```text
NAME        READY   UP-TO-DATE   AVAILABLE
chaos-api   2/2     2            2
```

The API service was exposed locally using port-forwarding:

```bash
kubectl port-forward -n chaos-sandbox service/chaos-api-service 8000:8000
```

The test endpoint was:

```text
http://127.0.0.1:8000/health
```

---

## Test Method

A request loop was started from the local machine.

Command used:

```bash
for i in {1..60}; do
  echo -n "Request $i: "
  curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/health
  sleep 1
done
```

This sent one request per second for 60 seconds.

While the request loop was running, one API pod was manually deleted.

Example command:

```bash
kubectl delete pod <ONE_API_POD_NAME> -n chaos-sandbox
```

This simulated the failure of one API pod while the system was actively receiving traffic.

---

## Failure Injected

One running API pod was deleted manually.

This simulated a pod-level application failure.

In a real production environment, this could represent:

- Application crash
- Container runtime issue
- Node disruption
- Manual operational mistake
- Failed pod caused by deployment issue

---

## Expected Result

The API should continue responding successfully because a second API pod remains available.

Expected behavior:

```text
One API pod terminates
Another API pod remains Running
Kubernetes creates a replacement pod
The Service continues routing to available pods
Requests continue returning HTTP 200
```

---

## Actual Request Results

All 60 requests returned HTTP `200`.

```text
Request 1: 200
Request 2: 200
Request 3: 200
Request 4: 200
Request 5: 200
Request 6: 200
Request 7: 200
Request 8: 200
Request 9: 200
Request 10: 200
Request 11: 200
Request 12: 200
Request 13: 200
Request 14: 200
Request 15: 200
Request 16: 200
Request 17: 200
Request 18: 200
Request 19: 200
Request 20: 200
Request 21: 200
Request 22: 200
Request 23: 200
Request 24: 200
Request 25: 200
Request 26: 200
Request 27: 200
Request 28: 200
Request 29: 200
Request 30: 200
Request 31: 200
Request 32: 200
Request 33: 200
Request 34: 200
Request 35: 200
Request 36: 200
Request 37: 200
Request 38: 200
Request 39: 200
Request 40: 200
Request 41: 200
Request 42: 200
Request 43: 200
Request 44: 200
Request 45: 200
Request 46: 200
Request 47: 200
Request 48: 200
Request 49: 200
Request 50: 200
Request 51: 200
Request 52: 200
Request 53: 200
Request 54: 200
Request 55: 200
Request 56: 200
Request 57: 200
Request 58: 200
Request 59: 200
Request 60: 200
```

Summary:

| Metric | Result |
|---|---|
| Total requests sent | `60` |
| Successful responses | `60` |
| Failed responses | `0` |
| Success rate | `100%` |
| Test endpoint | `/health` |
| HTTP success code | `200` |

---

## Kubernetes State After Recovery

After one API pod was deleted, Kubernetes created a replacement pod.

Observed pod status:

```text
NAME                             READY   STATUS    RESTARTS   AGE
chaos-api-b8b88ddf9-2mtj4        1/1     Running   0          20m
chaos-api-b8b88ddf9-wxrwl        1/1     Running   0          92s
chaos-postgres-5d4778d86-qpddz   1/1     Running   0          27m
chaos-redis-7cb6577fc6-l9wfc     1/1     Running   0          27m
```

Observed Deployment status:

```text
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
chaos-api   2/2     2            2           27m
```

Deployment details confirmed:

```text
Replicas: 2 desired | 2 updated | 2 total | 2 available | 0 unavailable
```

This confirms that Kubernetes restored the Deployment back to the desired state of two available API replicas.

---

## Recovery Evidence

The Deployment conditions showed that the new ReplicaSet was available.

```text
Conditions:
  Type           Status  Reason
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
```

The ReplicaSet confirmed that two replicas were created:

```text
NewReplicaSet: chaos-api-b8b88ddf9 (2/2 replicas created)
```

The Kubernetes events showed the Deployment scaling history:

```text
Events:
  Type    Reason             From                   Message
  Normal  ScalingReplicaSet  deployment-controller  Scaled up replica set chaos-api-b8b88ddf9 from 0 to 1
  Normal  ScalingReplicaSet  deployment-controller  Scaled up replica set chaos-api-b8b88ddf9 from 1 to 2
```

---

## Result Summary

| Check | Result |
|---|---|
| Two API replicas running before test | Yes |
| Continuous request loop started | Yes |
| One API pod deleted during request loop | Yes |
| Remaining API pod stayed running | Yes |
| Kubernetes created replacement pod | Yes |
| Deployment returned to `2/2` available | Yes |
| All 60 requests returned HTTP 200 | Yes |
| Failed requests observed | No |
| PostgreSQL remained running | Yes |
| Redis remained running | Yes |

---

## What This Proves

This test proves that scaling the API from one replica to two replicas improved service availability during pod failure.

The earlier pod failure test showed that Kubernetes could recreate a deleted pod.

This test showed something stronger:

```text
The service continued responding successfully while pod recovery happened.
```

The Kubernetes Service was able to route traffic to an available API pod while Kubernetes replaced the deleted pod.

This is a practical example of resilience through redundancy.

---

## Why This Matters

In production systems, availability is not only about whether a failed component can recover.

Availability is also about whether users are affected while recovery is happening.

With one API replica:

```text
If the only pod fails, users may experience temporary failure.
```

With two API replicas:

```text
If one pod fails, another pod can continue serving requests.
```

This is an important DevOps and SRE concept.

It shows that resilience can be improved through:

- Multiple replicas
- Kubernetes Services
- Readiness probes
- Automated pod replacement
- Clear failure testing

---

## Lessons Learned

| Concept | Lesson |
|---|---|
| Replicas | Running multiple replicas improves service availability |
| Kubernetes Service | Can route traffic to available pods |
| Deployment | Restores the desired number of replicas |
| Readiness Probe | Helps ensure only ready pods receive traffic |
| Failure Testing | Validates whether design improvements actually work |
| Availability Testing | Request loops provide stronger evidence than pod status alone |

This experiment showed the difference between infrastructure recovery and user-facing availability.

---

## Limitation of This Test

This test was performed in a local Kind cluster using `kubectl port-forward`.

That means it is a strong local validation, but not a complete production-grade availability test.

Current limitations:

- Local laptop environment
- Kind cluster instead of managed cloud Kubernetes
- `kubectl port-forward` instead of LoadBalancer or Ingress
- Simple `/health` endpoint only
- No Prometheus metrics yet
- No Grafana dashboard yet
- No automated MTTR calculation yet
- No production traffic simulation tool yet

Despite these limitations, the test is useful because it validates the basic Kubernetes resilience pattern.

---

## Future Improvements

Recommended next improvements:

- Repeat the same test against `/ready`.
- Add a script to automate the request loop and summarize failures.
- Add Prometheus metrics.
- Add Grafana dashboards.
- Add request latency tracking.
- Add MTTR measurement.
- Add Kubernetes Redis failure test.
- Add Kubernetes PostgreSQL failure test.
- Add LitmusChaos or Chaos Mesh.
- Repeat the test in Azure AKS or Google GKE later.
- Capture screenshots from Grafana once observability is added.

---

## Portfolio Value

This experiment is valuable for a DevOps and Cloud Support portfolio because it shows more than basic Kubernetes deployment.

It demonstrates:

```text
Deploy system
 ↓
Improve replica count
 ↓
Inject pod failure
 ↓
Send live requests during failure
 ↓
Confirm user-facing availability
 ↓
Document evidence
```

This is the type of practical reasoning used in DevOps, Cloud Support, Platform Engineering, and Site Reliability Engineering.

It shows the ability to think beyond “is the pod running?” and ask a better question:

```text
Can users still reach the service while failure is happening?
```

---

## Final Result

The two-replica API availability test passed.

All 60 requests returned HTTP `200` while one API pod was deleted and Kubernetes restored the Deployment to two available replicas.

```text
Final result: PASS
Success rate: 100%
Requests passed: 60/60
Requests failed: 0/60
```
