from acp_sdk.server import Server , Context, RedisStore
from acp_sdk.models import Message
from redis.asyncio import Redis # pip install redis


redis = Redis(
    host="127.0.0,1",
    port=6379,
    username="user", # read from a secret manager
    password="123", # read from a secret manager
    db="unique-database-name"
)

server = Server()

@server.agent("myagent")
async def myagent(input: Message, context:Context) : 
    history = context.session.load_history() 
    pass

server.run(store=RedisStore(store=redis))