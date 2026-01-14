from a2a.server.agent_execution import AgentExecutor , RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

class HelloWorldAgent:
    async def invoke(self) -> str:
        return "Hello World"

class HelloWorldAgentExecutor (AgentExecutor):
    def __init__(self):
        self.agent = HelloWorldAgent()
    
    async def execute(
            self,
            context: RequestContext,
            event_queue : EventQueue,
    ) -> None:
            result = await self.agent.invoke()
            message = new_agent_text_message(result)
            await event_queue.enqueue_event(result)
    
    async def cancel(
              self,
              context: RequestContext,
              event_queue : EventQueue,
    ) -> None:
            raise Exception("Cancellation is not supported.")