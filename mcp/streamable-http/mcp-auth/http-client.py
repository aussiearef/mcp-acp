import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from fastmcp.client.auth import BearerAuth # pip install fastmcp

token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImVtYWlsIjoiam9obi5kb2VAZXhhbXBsZS5jb20ifQ.KYsXTjBEkhzQS-nqFskrLwfXjEDZvKFtTBojESCpXwRj2u9B_Hcke8wTjdxnG8M9bAIFAVVkwvkHvU8WigXAyk6BG4zT6MC6_3xhqLeMI-kpSnCDP59rwO-ozPH7vQL5KB9kEdrlVVU5w1s_ePui0xWMks1yjYDVs7QEi3oC9_e2Y8zRZFjvhSgdboAoNJh2xtjLR7ozxcDXpXGLecG8fVe2B_gV1bCxOeTE3jQ-EKljOOfzm2TWyCY9Ui0rrrr8TlfMtxW__nTvGG9WKUIsMp9G_Cxb7skcwtjZTqFcvbyZEE-MuvcANrdxIBJ0wT1xwORkqQXjOIrMLNhxrlRg1_xAh5knS0ijvsv7wVWIKbAU0eVwNGP7RGvU9AzdJtnG69TGpIVGpXD1f01-BZzmeKr-WBOCMgemYPtNMNdJfQtvp4weNqkTERrrkRqNt9ezUZyi2eslh6TrQx4-6506w7tAeF2TbNiuoERSpHEZfL7DNH5m-ZvGSs46u1UyuNMYWJSTfwm5uUDGyl5ykriccSjv3q34gGWE3e8FxzeMBLdXlEjH8m15ZmwblaLPM_FBl8FsiddaWb10qQ3ZrdMrgVf-hOjgXcHNOzlQn2RQmIjcTu3BTHQhRs4Lj63aAPCifP-R9iYBCzKzatH5T-GKlE72VHHUmVa4sLb_wyP_HGk"
async def main():
    async with streamablehttp_client("http://localhost:8000/mcp", 
                                     auth=BearerAuth(token=token)) as (
        read_stream,
        write_stream,
        _, 
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Available tools:{[tool.name for tool in tools.tools]}")
            
            greeting_tool = next((tool for tool in tools.tools if tool.name == "Greetings"), None)
            if greeting_tool:
                tool_result = await session.call_tool(name="Greetings",
                                  arguments={"name":"Aref"})
                greeting = tool_result.structuredContent # other result types are EmbeddedResource and ImageContent
                print(greeting.get("message"))

if __name__=="__main__":
    asyncio.run(main())