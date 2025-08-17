
import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart


async def example() -> None:
    number="0498765432"
    async with Client(base_url="http://localhost:9000", headers={"x-api-key":"123"}) as client:
        run = await client.run_sync(agent="SimAssistant", input=Message(parts=[MessagePart(content=f"Please activate my sim card .  My mobile number is 0498765432")]))
        #run = await client.run_sync(agent="SimAssistant", input=Message(parts=[MessagePart(content=f"buy me a coffee")]))
        print(run.output[0].parts[0].content)



if __name__ == "__main__":
    asyncio.run(example())
