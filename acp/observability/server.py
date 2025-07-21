from acp_sdk.server import Server
from acp_sdk.models import Message

from beeai_framework.backend.chat import ChatModel # only needed if Agent is using LLM
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory

from opentelemetry import metrics 
from opentelemetry._logs import get_logger , LogRecord


server = Server()

meter = metrics.get_meter(name="otel.acp.example.metric")
request_counter = meter.create_counter(
    "otel.meaningagent.run_count",
    description="Total requests processed",
    unit="1"
)

logger = get_logger("ACP Server")
logger.emit(LogRecord(
    body="Starting ACP Server"
))

@server.agent("MeaningAgent")
async def meaning(words: Message) -> str:
    
    request_counter.add(1, {"agent": "MeaningAgent"})

    logger.emit("Calling OPEN AI")
    llm= ChatModel.from_name("openai:gpt-4o")  

    memory = TokenMemory(llm)
    agent = ReActAgent(llm=llm, tools=[], memory=memory)
    response = await agent.run(prompt=f"Find the meaning of the word: {words[0]}. Be concise and return one sentence.",)
    return response.result.text

server.run(configure_telemetry=True) 