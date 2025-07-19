from acp_sdk.server import Server, Context, PostgreSQLStore
from acp_sdk.models import Message
from psycopg import AsyncConnection # pip install psycopg

aconn = AsyncConnection.connect(
    "postgresql://user:password@host:5432/database",
)

server = Server()

@server.agent("myagent")
async def myagent(input: Message, context: Context) :
    history = context.session.load_history() 
    pass


server.run(store=PostgreSQLStore(aconn=aconn, table="unique-table"))

