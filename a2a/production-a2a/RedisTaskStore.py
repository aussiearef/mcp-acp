
import json
import redis.asyncio as redis
from a2a.server.context import ServerCallContext
from a2a.server.tasks.task_store import TaskStore
from a2a.types import Task

class RedisTaskStore(TaskStore): # type: ignore
    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url, decode_responses=True)

    async def save(self, task: Task, context: ServerCallContext | None = None) -> None:
        task_json = task.model_dump_json()
        await self.client.set(f"task:{task.task_id}", task_json)

    async def get(self, task_id: str, context: ServerCallContext | None = None) -> Task | None:
        data = await self.client.get(f"task:{task_id}")
        if not data:
            return None
        from a2a.types import Task
        return Task.model_validate_json(data)

    async def delete(self, task_id: str, context: ServerCallContext | None = None) -> None:
        await self.client.delete(f"task:{task_id}")