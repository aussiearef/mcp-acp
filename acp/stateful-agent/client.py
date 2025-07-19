import asyncio

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

async def session_example() -> None:
    async with Client(base_url="http://localhost:8000") as client, client.session() as session:
        run = await session.run_sync(agent="chat", input=[Message(parts=[MessagePart(content="Hello, my name is Aref!")])])
        run = await session.run_sync(agent="chat", input=[Message(parts=[MessagePart(content="Say a joke, with my name in it!")])])

        print(run.output[0].parts[0].content)

if __name__ == "__main__":
    asyncio.run(session_example())