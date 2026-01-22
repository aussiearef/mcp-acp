from fastmcp import FastMCP 
from pydantic import BaseModel
import asyncio

mcp = FastMCP()

class Greeting(BaseModel):
    message: str

@mcp.tool("Greetings")
def greetings (name:str) -> Greeting:
    """A tool function that accepts a parameter called name and returns a personalised greeting message."""

    return  Greeting(message= f"Hello, {name}")

async def main():
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())