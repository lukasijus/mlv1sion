# app/core/observability.py
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Request, Response
import time

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "HTTP request latency", ["path", "method", "status"]
)
REQUEST_COUNT = Counter(
    "http_request_total", "Total HTTP requests", ["path", "method", "status"]
)


async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response: Response = await call_next(request)
    elapsed = time.time() - start
    REQUEST_LATENCY.labels(
        path=request.url.path, method=request.method, status=response.status_code
    ).observe(elapsed)
    REQUEST_COUNT.labels(
        path=request.url.path, method=request.method, status=response.status_code
    ).inc()
    return response
