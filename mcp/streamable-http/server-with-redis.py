from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel
import asyncio
import redis

# mcp = FastMCP(stateless_http=True)
mcp = FastMCP()

class Greeting(BaseModel):
    message: str

@mcp.tool("Greetings")
def greetings (name:str , ctx: Context) -> Greeting:
    """A tool function that accepts a parameter called name and returns a personalised greeting message."""

    session_id = ctx.session_id

    redis_client = redis.Redis(host='localhost', port=6379, username="", password="")

    stored_name = redis_client.get(session_id)

    if stored_name == None:
        redis_client.set(session_id, name)
    else:
        name = stored_name.decode('utf-8')

    ctx.info("Returning results..") # Use Context to generate Logs

    return  Greeting(message= f"Hello, {name}")

async def main():
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())