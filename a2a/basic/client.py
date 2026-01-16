import asyncio
import httpx
from uuid import uuid4

from a2a.types import Message , TextPart
from a2a.client import ClientFactory , ClientConfig
from a2a.client.card_resolver import A2ACardResolver

async def main():
    server_url = "http://localhost:9999"

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client= httpx_client,
            base_url= server_url,
            agent_card_path="/.well-known/agent-card.json"
        )

        agent_card = await resolver.get_agent_card()

        config = ClientConfig(httpx_client= httpx_client)
        factory = ClientFactory(config=config)
        client = factory.create(card=agent_card)

        user_message = Message(
            role="user",
            parts=[TextPart(text="Hello, Agent.")],
            message_id=uuid4().hex
        )

        response = client.send_message(user_message)
        async for response_event in response:
            for part in response_event.parts:
                model_dict = part.model_dump()
                print(model_dict['text'])

if __name__=="__main__":
    asyncio.run(main())