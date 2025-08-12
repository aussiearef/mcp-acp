# server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import random

app = FastMCP(name="observability-mcp", host="0.0.0.0", port=8000)

# ===== Models =====
class Alert(BaseModel):
    id: str
    service: str        # always "orders-api"
    kind: str           # "high_cpu" | "high_memory_utilisation" | "low_disk_space"
    severity: str       # "low" | "medium" | "high"

class SeriesPoint(BaseModel):
    t: str              # ISO-8601 (Z)
    v: float            # percentage

class MetricsResponse(BaseModel):
    service: str        # always "orders-api"
    metric: str         # "cpu" | "memory" | "disk"
    series: list[SeriesPoint]

class LogEntry(BaseModel):
    t: str
    level: str
    msg: str

class LogsResponse(BaseModel):
    service: str       
    level: str
    lines: list[LogEntry]


def iso_now_minus(minutes: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")


def _dump(m):
    # Pydantic v2 uses .model_dump(); v1 uses .dict()
    return m.model_dump() if hasattr(m, "model_dump") else m.dict()

@app.tool(name="list_alerts", title="List current alerts for orders-api.")
def list_alerts() -> list[dict]:
    alerts = [
        Alert(id="A-CPU-1001",  service="orders-api", kind="high_cpu",                severity="high"),
        Alert(id="A-MEM-1002",  service="orders-api", kind="high_memory_utilisation", severity="medium"),
        Alert(id="A-DISK-1003", service="orders-api", kind="low_disk_space",          severity="medium"),
    ]
    return [_dump(a) for a in alerts]

@app.tool(name="get_metrics", title="Return a small synthetic series for orders-api.")
def get_metrics(metric: str) -> MetricsResponse:

    base_map = {"cpu": 55, "memory": 60, "disk": 80}
    base = base_map.get(metric, 50)
    series: list[SeriesPoint] = []

    for i in range(12):
        extra = 0.0
        if metric == "cpu" and i >= 8:
            extra = 30                   
        if metric == "memory" and i >= 9:
            extra = 15                  
        if metric == "disk" and i >= 6:
            extra = (i - 5) * 2         
        val = max(0, min(100, base + extra + random.uniform(-2, 2)))
        series.append(SeriesPoint(t=iso_now_minus(12 - i), v=val))

    return MetricsResponse(service="orders-api", metric=metric, series=series)

@app.tool(name="get_logs", title="Return a few recent log lines for orders-api.")
def get_logs() -> LogsResponse:
    messages = [
        "worker saturation; throttling requests",
        "timeout calling inventory-service",
        "db connection pool exhausted",
        "retry budget exceeded",
        "gc pause > 500ms",
        "failed to write cache file",
    ]
    lines = [LogEntry(t=iso_now_minus(i + 1), msg=random.choice(messages)) for i in range(6)]
    return LogsResponse(service="orders-api",  lines=lines)


if __name__ == "__main__":
   app.run(transport="streamable-http")
