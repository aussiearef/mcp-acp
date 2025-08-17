import os
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from acp_sdk.models import Message, ACPError,  Error
from acp_sdk.server import create_app, agent, Context

from beeai_framework.backend.chat import ChatModel
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.tools import AnyTool
from beeai_framework.tools.mcp import MCPTool 

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


mcp_url = os.environ.get("MCP_URL", "http://localhost:8000/mcp/")

@agent(name="SimAssistant",
    description="Activate Australian SIMs. MCP is used only to fetch SIM status.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"])
async def sim_assistant(msg: Message,  context:Context) -> str:
    user_text = str(msg[0])
    
    try:
        await authenticate(context)
    except ACPError as e:
        return str(e)
    

    mcp_api_key = os.environ.get("mcp_api_key")
    if mcp_api_key==None:
        raise ACPError("Please provide the mcp_api_key environment variable.")

    # Connect to MCP and fetch status tool
    async with streamablehttp_client(mcp_url, 
                headers={"x-api-key":mcp_api_key}       
                ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            mcp_tools: List[AnyTool] = await MCPTool.from_client(session=session)
            
            # Find MCP tools
            get_status_tool = next(
                (t for t in mcp_tools if t.name == "get_number_status"), None
            )

            set_status_tool = next(
                (t for t in mcp_tools if t.name == "set_number_status"), None
            )
        
            # LLM + memory (BeeAI ReAct pattern)
          
            llm = ChatModel.from_name("openai:gpt-4o-mini")
            memory = TokenMemory(llm)

            tools = [get_status_tool, set_status_tool]

            system_prompt = (
                "You are a Mobile SIM activation assistant working in a Telco.\n"
                "Follow below instructions precisely to respond to user's SIM Card or Mobile activation or deactivation request:\n"
                "If user is asking anything other than activating a SIM or mobile number, respond that you can only do SIM activation\n"
                "1) If the user wants SIM activation or deactivation, but has not provided a mobile number, ask: 'What is your mobile number?'\n"
                "2) If mobile number is provided, make sure it is in Australian format . If not, don't proceed.\n"
                "3) If a valid mobile number then get the SIM's status:"
                "   - If SIM status = 'active' then reply exactly: 'your sim is already active'.\n"
                "   - If SIM status = 'inactive' then call activate_sim with {number}, then rreply exactly: 'Your SIM was activated.'\n"
                "   - If SIM status = 'not_found' then reply exactly: 'Mobile number not found'.\n"
                "If word 'error' is found in the tool's response , respond with that message and do not proceed.\n"
                "only reply with the responses I have specified."
            )

            agent = ReActAgent(llm=llm, tools=tools, memory=memory)
            response = await agent.run(prompt=f"{system_prompt} . user's prompt is: {user_text}")
            return response.result.text


async def authenticate(ctx: Context):
    auth_header = ctx.request.headers.get("x-api-key")
    acp_api_key= os.environ.get("acp_api_key")
    if acp_api_key == None :
        raise ACPError(Error(code="401", message="acp_api_key is missing!"))
    
    if auth_header != acp_api_key:
        raise ACPError(Error(code="401", message="Authentication key not provided"))

if __name__ == "__main__":

    
    app = create_app(sim_assistant)
    server = CORSMiddleware(
        app=app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(server, host="0.0.0.0", port=9000)