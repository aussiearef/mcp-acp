from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from SimAssistantExecutor import SimAssistantExecutor
from fastapi.middleware.cors import CORSMiddleware

if __name__ == "__main__":

    agent_skill = AgentSkill(
        id="sim_activation_skill",
        name="SIM Activation",
        description="Activate or deactivate SIM cards",
        tags=["SIM", "Activation", "Telco"]
    )

    agent_capabilities = AgentCapabilities(
        streaming=False
    )

    agent_card = AgentCard(
        name="SimAssistant",
        description="Activate Australian SIMs using MCP-backed tools",
        version="1.0",
        url="http://localhost:9000",
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[agent_skill],
        capabilities=agent_capabilities
    )

    request_handler = DefaultRequestHandler(
        agent_executor=SimAssistantExecutor(),
        task_store=InMemoryTaskStore()
    )

    server = A2AFastAPIApplication(
        http_handler=request_handler,
        agent_card=agent_card
    ).build()

    server.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    import uvicorn
    uvicorn.run(
        server,
        host="0.0.0.0",
        port=9000
    )
