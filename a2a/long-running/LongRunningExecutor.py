import asyncio
from uuid import uuid4

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TextPart,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    TaskState,
    Artifact
)

class LongRunningExecutor(AgentExecutor):
    async def execute(
            self,
            context: RequestContext,
            event_queue: EventQueue
    )->None:
        # 1. Read input from context
        user_text=""
        if context.message.parts:
            user_text= getattr(context.message.parts[0] , 'text', '')
        
        # 2. Signal Task Submitted
        await event_queue.enqueue_event(TaskStatusUpdateEvent(
            task_id= context.task_id,
            status=TaskState.submitted,
            metadata="Submitted...",
            final=False
        ))

        # 3. Simulate work with status and artifact updates
        for i in range (1,4):
                await event_queue.enqueue_event(TaskStatusUpdateEvent(
                task_id= context.task_id,
                status=TaskState.working,
                metadata="Working...",
                final=False
             ))

                await asyncio.sleep(2) # Long running work

                artifact = Artifact(uuid4().hex , name="Artifact", description="Partial Result")
                artifact.parts.append(TextPart('This is part of the result'))

                await event_queue.enqueue_event(TaskArtifactUpdateEvent(
                    task_id= context.task_id,
                    context_id=context.context_id,
                    artifact=artifact

                ))
        
        # 4. Return final status
        # 5. Signal Task Submitted
        await event_queue.enqueue_event(TaskStatusUpdateEvent(
            task_id= context.task_id,
            status=TaskState.completed,
            metadata="Completed...",
            final=True
        ))

    async def cancel(self, context:RequestContext, event_queue:EventQueue) -> None:
         pass



