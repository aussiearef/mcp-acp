# server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

app = FastMCP(name="observability-mcp", host="0.0.0.0" , port=8000)

class Alert(BaseModel):
    id: str
    service: str
    env: str
    kind: str
    severity: str
    started_at: str

class SeriesPoint(BaseModel):
    t: str
    v: float

class MetricsResponse(BaseModel):
    service: str
    metric: str
    window: str
    series: list[SeriesPoint]

class LogEntry(BaseModel):
    t: str
    level: str
    msg: str

class LogsResponse(BaseModel):
    service: str
    level: str
    window: str
    lines: list[LogEntry]

class Incident(BaseModel):
    id: str
    summary: str
    severity: str
    status: str = "OPEN"

@app.tool(name="list_alerts", title="Returns the list of all alerts.")
def list_alerts(env: str) -> list[Alert]:
    now = datetime.now(datetime.timetzone.utc)
    return [
        Alert(
            id="A-1001", service="orders-api", env=env, kind="cpu_high",
            severity="high", started_at=(now - timedelta(minutes=12)).isoformat()+"Z"
        ),
        Alert(
            id="A-1002", service="payments", env=env, kind="latency_spike",
            severity="medium", started_at=(now - timedelta(minutes=30)).isoformat()+"Z"
        ),
    ]

@app.tool(name="get_metrics", title="returns the metrics of orders-api.")
def get_metrics(service: str, metric: str, window: str) -> MetricsResponse:
    # Generate 15m of 1-min points with a spike
    now = datetime.utcnow()
    points = []
    for i in range(15):
        t = (now - timedelta(minutes=15-i)).isoformat()+"Z"
        base = 35 if service != "orders-api" else 55
        spike = 40 if (service=="orders-api" and i>10) else 0
        val = base + spike + random.uniform(-3, 3)
        points.append(SeriesPoint(t=t, v=max(0, min(100, val))))
    return MetricsResponse(service=service, metric=metric, window=window, series=points)

@app.tool(name="get_logs", title="returns log entries of orders-api.")
def get_logs(service: str, level: str, window: str) -> LogsResponse:
    now = datetime.utcnow()
    msgs = [
        "timeout from inventory-service",
        "db connection pool exhausted",
        "upstream 502 from pricing",
        "retry budget exceeded"
    ]
    lines = [
        LogEntry(t=(now - timedelta(minutes=i)).isoformat()+"Z", level=level, msg=random.choice(msgs))
        for i in range(1, 9)
    ]
    return LogsResponse(service=service, level=level, window=window, lines=lines)

@app.tool(name="open_incident", title="creates an incident if alert is persistent in orders-api.")
def open_incident(summary: str, severity: str) -> Incident:
    return Incident(id=f"INC-{random.randint(2000,9999)}", summary=summary, severity=severity)

if __name__ == "__main__":
    # Default: listens on 0.0.0.0:8000 and exposes /mcp
    app.run(transport='streamable-http')
