# Incident Report 01 — Redis Manual Failure Test

## Experiment Name

Redis Manual Failure Test

## Date

June 2026

## Purpose

This experiment tested how the API behaves when the Redis cache dependency becomes unavailable.

The goal was to confirm that the API can detect a failed dependency and report the system as **not ready** instead of pretending everything is healthy.

---

## System State Before Failure

The application was running locally using Docker Compose.

Active containers:

```text
chaos-api
chaos-postgres
chaos-redis
```

The `/ready` endpoint showed that both PostgreSQL and Redis were reachable.

Expected status:

```json
{
  "status": "ready",
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

---

## Failure Injected

Redis was manually stopped using Docker:

```bash
docker stop chaos-redis
```

This simulated a cache service failure.

---

## Expected Result

The API should remain alive, but readiness should change from:

```text
ready
```

to:

```text
not_ready
```

Redis should be reported as:

```text
unreachable
```

---

## Actual Result

After Redis was stopped, the `/ready` endpoint reported that Redis was unreachable.

The API container continued running.

This means the application was able to detect dependency failure without crashing completely.

---

## Recovery Action

Redis was restarted using Docker:

```bash
docker start chaos-redis
```

After Redis restarted, the `/ready` endpoint returned to a ready state.

---

## Result Summary

| Item | Result |
|---|---|
| API stayed alive | Yes |
| Redis failure detected | Yes |
| Readiness status changed | Yes |
| System recovered after Redis restart | Yes |
| Manual recovery required | Yes |

---

## Lessons Learned

This test showed the difference between a **health check** and a **readiness check**.

The `/health` endpoint confirms that the API process is alive.

The `/ready` endpoint confirms whether the API is ready to serve traffic based on dependency availability.

This is important in Kubernetes because readiness checks help prevent traffic from being sent to pods that are alive but not fully ready.

---

## Future Improvement

Future chaos experiments should measure:

- How long Redis was unavailable
- How long the API took to report recovery
- Whether users would experience errors
- Whether alerts can be triggered automatically
- Whether the system can degrade gracefully when cache is unavailable

---

## Portfolio Value

This report demonstrates an early resilience test in the project.

Even though this was a manual failure test rather than a full chaos engineering experiment, it proves that the application can:

- Detect dependency failure
- Report readiness accurately
- Continue running when Redis is unavailable
- Recover after the dependency is restored

This is the foundation for future Kubernetes-based chaos experiments.
