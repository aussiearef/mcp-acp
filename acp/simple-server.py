from acp_sdk.server import Server
from acp_sdk.models import Message

server = Server()

@server.agent("NameAgent")
async def nameagent(names: Message) -> str:
    return f"Hello, {names[0]}!"

server.run(port=8000)