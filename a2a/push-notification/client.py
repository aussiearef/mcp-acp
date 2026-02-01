import asyncio
import httpx
import uvicorn
from pydantic import TypeAdapter
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi import Header, HTTPException

from a2a.types import Message, TextPart, PushNotificationConfig , PushNotificationAuthenticationInfo
from a2a.client import ClientFactory, ClientConfig
from a2a.client.card_resolver import A2ACardResolver
from a2a.types import TaskStatusUpdateEvent, TaskArtifactUpdateEvent

A2AEvent = TaskStatusUpdateEvent | TaskArtifactUpdateEvent
event_adapter = TypeAdapter(A2AEvent)

app = FastAPI()

SERVER_URL = "http://localhost:9999"
CALLBACK_URL = "http://localhost:8000/notifications"
API_KEY="YOUR API KEY"

@app.post("/notifications")
async def handle_push_notification(
    request: Request, 
    x_api_key: str | None = Header(None) 
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorised")

    payload = await request.json()
    
    event = event_adapter.validate_python(payload)
        
    if isinstance(event, TaskStatusUpdateEvent):
        print(f"Status: {event.status.state} - {event.metadata.get('info')}")
    
    elif isinstance(event, TaskArtifactUpdateEvent):
        print(f"Artifact Received: {event.artifact.name}")

    return {"status": "ok"}


async def initiate_agent_request():
    await asyncio.sleep(2)
    
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=SERVER_URL,
            agent_card_path="/.well-known/agent-card.json"
        )

        agent_card = await resolver.get_agent_card()
        config = ClientConfig(httpx_client=httpx_client)
        factory = ClientFactory(config=config)
        client = factory.create(card=agent_card)

        notification_cfg = PushNotificationConfig(
            url=CALLBACK_URL,
            authentication=PushNotificationAuthenticationInfo( 
                schemes=["Basic"] ,
                credentials=API_KEY
            )) 

        user_message = Message(
            role="user",
            parts=[TextPart(text="Execute long task with push.")],
            message_id=uuid4().hex
        )
        response = client.send_message(
            user_message, 
            notification_config=notification_cfg # Signals server to use Push Notifications
        )

        async for response_event in response:
            # You can still stream events here while the server 
            # also sends them to your /notifications endpoint
            for part in response_event.parts:
                print(f"Streamed: {part.model_dump().get('text')}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(initiate_agent_request())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)