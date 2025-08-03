import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI 
from mcp import ClientSession,types
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import TextContent
from mcp.shared.context import RequestContext

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def sampling_handler(context: RequestContext, params: types.CreateMessageRequestParams) -> types.CreateMessageResult:
    prompt_text = params.messages[0].content.text
    
    # Call LLM 
    response = await llm_client.chat.completions.create(
        model="gpt-4o", 
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt_text}]
    )
    llm_output = response.choices[0].message.content

    return types.CreateMessageResult(
        role="assistant",
        content=TextContent(type="text", text=llm_output),
        model="gpt-4o" 
    )

async def main():
    server_url = "http://localhost:8000/mcp"
    topic = input("Enter a topic for a poen:")
    async with streamablehttp_client(server_url) as (
        read_stream,
        write_stream,
        _, 
    ):
        async with ClientSession(read_stream, write_stream, sampling_callback=sampling_handler) as session:
            await session.initialize()
            tool_result = await session.call_tool(name="generate_poem",
                                  arguments={"topic": topic})
            print(tool_result.content[0].text) 


if __name__ == "__main__":
    asyncio.run(main())

