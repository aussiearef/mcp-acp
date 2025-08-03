import os
import asyncio
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from fastmcp.client.auth import BearerAuth

async def get_bearer_token(client_id: str, client_secret: str, token_endpoint: str, scopes: list[str] = None) -> str:
    """Obtain a Bearer token using Client Credentials Grant."""
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience":"https://dev-of6fy7icbrna3p24.us.auth0.com/api/v2/"
        }
        response = await client.post(
            token_endpoint,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        token_data = response.json()
        return token_data["access_token"]

async def main():
    # Google OAuth 2.0 provider details
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token_endpoint = "https://dev-of6fy7icbrna3p24.us.auth0.com/oauth/token"  #  token endpoint
    scopes = None

    token = await get_bearer_token(client_id, client_secret, token_endpoint, scopes)
    print(token)
    # Connect to MCP server with the obtained token
    async with streamablehttp_client(
        "http://localhost:8000/mcp",
        auth=BearerAuth(token=token)
    ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            greeting_tool = next((tool for tool in tools.tools if tool.name == "Greetings"), None)
            if greeting_tool:
                tool_result = await session.call_tool(name="Greetings", arguments={"name": "Aref"})
                greeting = tool_result.structuredContent
                print("Greeting:", greeting.get("message"))

if __name__ == "__main__":
    asyncio.run(main())