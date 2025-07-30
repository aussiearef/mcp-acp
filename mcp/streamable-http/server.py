from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import asyncio

mcp = FastMCP(stateless_http=True)

class Greeting(BaseModel):
    message: str

@mcp.tool("Greetings")
def greetings (name:str) -> Greeting:
    """A tool function that accepts a parameter called name and returns a personalised greeting message."""
    return  Greeting(message= f"Special greetings to, {name}")

#mcp.run(transport='streamable-http') # or use mcp.run_streamable_http_async()

async def main():
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())