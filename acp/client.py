
import asyncio

from acp_sdk.client import Client


async def example() -> None:
    async with Client(base_url="http://localhost:8000") as client:
        run = await client.run_sync(agent="MeaningAgent", input="Book")
        print(run.output[0].parts[0].content)


if __name__ == "__main__":
    asyncio.run(example())
