from acp_sdk.server import Server
from acp_sdk.models import Message, TrajectoryMetadata , MessagePart, AnyModel

from beeai_framework.backend.chat import ChatModel # only needed if Agent is using LLM
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory

server = Server()

@server.agent("MeaningAgent")
async def meaning(words: Message) -> str:
    llm= ChatModel.from_name("openai:gpt-4o")  

    memory = TokenMemory(llm)
    agent = ReActAgent(llm=llm, tools=[], memory=memory)
    response = await agent.run(prompt=f"Find the meaning of the word: {words[0]}. Be concise and return one sentence.",)
    text= response.result.text
    
    message= Message(parts=[MessagePart(
        content_type="text/plain",
        content=text,
        metadata=TrajectoryMetadata(
            tool_name="Name of MCP Server (tool) that was used.",
            tool_input=AnyModel(knowledge_base="SharePoint"),
            tool_output=AnyModel(domain="Finance"))
    )])

    return message

server.run() 