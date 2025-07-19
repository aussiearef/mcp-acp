
import asyncio
from acp_sdk.client import Client

async def example() -> None:
    async with Client(base_url="https://localhost:8000", verify=False) as client:  # Set verify=False for self-signed certificates only

        run = await client.run_sync(agent="NameAgent", input="Aref")
        print(run.output[0].parts[0].content)


if __name__ == "__main__":
    asyncio.run(example())
