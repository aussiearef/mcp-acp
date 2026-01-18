from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from RedisTaskStore import RedisTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from executor import (
    HelloWorldAgentExecutor
)

if __name__ =="__main__":
    agent_skill = AgentSkill(
        id="say_hello_skill",
        name="Hello Skill",
        description="I can say hello",
        tags=["Hello", "World"]
    )

    agent_capabiliy = AgentCapabilities(streaming=False)

    agent_card = AgentCard(
        name="Basic Server Agent (HelloWorld)",
        description="",
        version="1.0",
        url="http://localhost:9999",
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[agent_skill],
        capabilities=agent_capabiliy
    )

    redis_url="redis://localhost:6379/0" # Change to match your Redis configuration
    redis_task_store = RedisTaskStore(redis_url)

    request_handler = DefaultRequestHandler(
        agent_executor= HelloWorldAgentExecutor(),
        task_store= redis_task_store()
    )

    server = A2AFastAPIApplication(
        http_handler= request_handler,
        agent_card=agent_card
    )

    import uvicorn
    uvicorn.run(server.build() , host="0.0.0.0" , port=9999)