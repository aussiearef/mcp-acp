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
    env: str
    kind: str           # "high_cpu" | "high_memory_utilisation" | "low_disk_space"
    severity: str       # "low" | "medium" | "high"
    started_at: str     # ISO-8601 (Z)

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


@app.tool(name="list_alerts", title="List current alerts for orders-api.")
def list_alerts(env: str) -> list[Alert]:
    now12 = iso_now_minus(12)
    now25 = iso_now_minus(25)
    now40 = iso_now_minus(40)
    return [
        Alert(id="A-CPU-1001",  service="orders-api", env=env, kind="high_cpu",                 severity="high",   started_at=now12),
        Alert(id="A-MEM-1002",  service="orders-api", env=env, kind="high_memory_utilisation",  severity="medium", started_at=now25),
        Alert(id="A-DISK-1003", service="orders-api", env=env, kind="low_disk_space",           severity="medium", started_at=now40),
    ]

@app.tool(name="get_metrics", title="Return a small synthetic series for orders-api.")
def get_metrics(metric: str) -> MetricsResponse:

    base_map = {"cpu": 55, "memory": 60, "disk": 80}
    base = base_map.get(metric, 50)
    series: list[SeriesPoint] = []

    for i in range(12):
        extra = 0.0
        if metric == "cpu" and i >= 8:
            extra = 30                    # spike after point 8
        if metric == "memory" and i >= 9:
            extra = 15                    # rise near the end
        if metric == "disk" and i >= 6:
            extra = (i - 5) * 2           # rising utilization -> less free space
        val = max(0, min(100, base + extra + random.uniform(-2, 2)))
        series.append(SeriesPoint(t=iso_now_minus(12 - i), v=val))

    return MetricsResponse(service="orders-api", metric=metric, series=series)

@app.tool(name="get_logs", title="Return a few recent log lines for orders-api.")
def get_logs(level: str) -> LogsResponse:
    messages = [
        "worker saturation; throttling requests",
        "timeout calling inventory-service",
        "db connection pool exhausted",
        "retry budget exceeded",
        "gc pause > 500ms",
        "failed to write cache file",
    ]
    lines = [LogEntry(t=iso_now_minus(i + 1), level=level, msg=random.choice(messages)) for i in range(6)]
    return LogsResponse(service="orders-api", level=level, lines=lines)


if __name__ == "__main__":
    app.run(transport="streamable-http")
