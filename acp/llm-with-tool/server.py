from acp_sdk.server import Server
from acp_sdk.models import Message

from beeai_framework.backend.chat import ChatModel # only needed if Agent is using LLM
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.tools import AnyTool

from beeai_framework.tools.mcp import MCPTool 
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio


server = Server()

@server.agent("Greetings")
async def meaning(name: Message) -> str:
    """A tool function that accepts a parameter called name and returns a greeting message for that name."""

    async with streamablehttp_client("http://localhost:8000/mcp", ) as (
        read_stream,
        write_stream,
        _, 
    ):
        async with ClientSession(read_stream, write_stream) as session:
        
            mcp_tools = await MCPTool.from_client(session=session) 
            greeting_tool: list[AnyTool]  = list(filter(lambda tool: tool.name == "Greetings", mcp_tools))        

            llm= ChatModel.from_name("openai:gpt-4o")  

            memory = TokenMemory(llm)
            agent = ReActAgent(llm=llm, tools=greeting_tool, memory=memory)
            response = await agent.run(prompt=f"Create a greeting message for the a person called  {name[0]}.")
            return response.result.text
 
if __name__=="__main__":
    asyncio.run(server.run(port=9000))