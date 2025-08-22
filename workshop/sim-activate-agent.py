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

from authlib.jose import  JsonWebToken, JsonWebKey, JWTClaims
from authlib.jose.util import extract_header

import httpx


mcp_url = os.environ.get("MCP_URL", "http://localhost:8000/mcp/")

OAUTH_ISSUER = "https://accounts.google.com"
JWKS_URI = "https://www.googleapis.com/oauth2/v3/certs"
AUDIENCE = ""    # YOUR_GOOGLE_CLIENT_ID


@agent(name="SimAssistant",
    description="Activate Australian SIMs. MCP is used only to fetch SIM status.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"])
async def sim_assistant(msg: Message,  context:Context) -> str:
    user_text = str(msg[0])


    # Connect to MCP and fetch status tool
    async with streamablehttp_client(mcp_url, 
                                     headers={"x-api-key":"123"}) as (read_stream, write_stream, _):
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
    authorization_header = ctx.request.headers.get("Authorization")
    
    if authorization_header:
        token = authorization_header.removeprefix("Bearer ")
        token_obj = JsonWebToken(algorithms=["RS256"])
        
        #header = JWSHeader(header= token.split(".")[0], protected=None)
        header_segment = token.split(".")[0]
        header = extract_header(header_segment.encode("utf-8"), error_cls=ACPError)
        kid = header.get("kid")

        if not kid:
            raise ValueError("No kid in token header")

        jwk = await get_public_key(kid)
        public_key = JsonWebKey.import_key(jwk)

        # Decode the token with the public key. If signature invalid, exception is raised.
        claims: JWTClaims = token_obj.decode(token, public_key)
        # We do not read the claims. But if you want to check name, email ,id etc, you can read the claims.


async def get_public_key(kid: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URI)
        response.raise_for_status()
        keys = response.json()["keys"]

        for key in keys:
            if key["kid"] == kid:
                return key
        raise ValueError(f"No public key found for kid: {kid}")


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