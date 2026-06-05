#!/usr/bin/env bash

set -u

URL="${1:-http://127.0.0.1:8000/health}"
TOTAL_REQUESTS="${2:-60}"
SLEEP_SECONDS="${3:-1}"

SUCCESS_COUNT=0
FAILURE_COUNT=0

echo "=============================================="
echo "Chaos Engineering Sandbox - API Availability Check"
echo "=============================================="
echo "Target URL       : ${URL}"
echo "Total requests   : ${TOTAL_REQUESTS}"
echo "Delay per request: ${SLEEP_SECONDS}s"
echo "----------------------------------------------"

for i in $(seq 1 "${TOTAL_REQUESTS}"); do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${URL}" || echo "000")

  if [ "${HTTP_CODE}" = "200" ]; then
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    echo "Request ${i}: ${HTTP_CODE} OK"
  else
    FAILURE_COUNT=$((FAILURE_COUNT + 1))
    echo "Request ${i}: ${HTTP_CODE} FAILED"
  fi

  sleep "${SLEEP_SECONDS}"
done

SUCCESS_RATE=$(awk "BEGIN { printf \"%.2f\", (${SUCCESS_COUNT}/${TOTAL_REQUESTS})*100 }")

echo "----------------------------------------------"
echo "Availability Test Summary"
echo "----------------------------------------------"
echo "Target URL         : ${URL}"
echo "Total requests     : ${TOTAL_REQUESTS}"
echo "Successful requests: ${SUCCESS_COUNT}"
echo "Failed requests    : ${FAILURE_COUNT}"
echo "Success rate       : ${SUCCESS_RATE}%"

if [ "${FAILURE_COUNT}" -eq 0 ]; then
  echo "Final result       : PASS"
  exit 0
else
  echo "Final result       : FAIL"
  exit 1
fi
