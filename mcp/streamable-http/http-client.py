import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

# from mcp.client.stdio import stdio_client

async def main():
    async with streamable_http_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _, 
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            # await session.list_resources
            print(f"Available tools:{[tool.name for tool in tools.tools]}")
            
            greeting_tool = next((tool for tool in tools.tools if tool.name == "Greetings"), None)
            if greeting_tool:
                tool_result = await session.call_tool(name="Greetings",
                                  arguments={"name":"Aref"})
                greeting = tool_result.structuredContent # other result types are EmbeddedResource and ImageContent
                print(greeting.get("message"))

if __name__=="__main__":
    asyncio.run(main())