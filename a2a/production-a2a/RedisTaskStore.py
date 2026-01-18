import json
import redis.asyncio as redis
from a2a.server.tasks import TaskStore
from a2a.types import Task, ServerCallContext

class RedisTaskStore(TaskStore):
    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url, decode_responses=True)

    async def save(
        self, task: Task, context: ServerCallContext | None = None
    ) -> None:
        """Saves or updates a Task object in Redis."""
        task_json = task.model_dump_json()
        await self.client.set(f"task:{task.task_id}", task_json)

    async def get(
        self, task_id: str, context: ServerCallContext | None = None
    ) -> Task | None:
        """Retrieves and deserialises a Task from Redis."""
        data = await self.client.get(f"task:{task_id}")
        if not data:
            return None
        
        return Task.model_validate_json(data)

    async def delete(
        self, task_id: str, context: ServerCallContext | None = None
    ) -> None:
        """Deletes the task record from Redis."""
        await self.client.delete(f"task:{task_id}")