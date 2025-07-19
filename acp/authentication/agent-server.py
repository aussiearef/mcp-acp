from acp_sdk.server import Server,Context 
from acp_sdk.models import Message , Error, ACPError , ErrorCode

server=Server()

@server.agent("myagent")
async def myagent(input: Message , context:Context):
    auth_header = context.request.headers.get("authentication")
    if (auth_header == ""):
        raise ACPError(error=Error(
            code= ErrorCode(401),
            message= "Authentication header not found."
        ))

    if (str.startswith("bearer") != True):
        raise ACPError()
    
    # Write custom code to validatte the authentication token
    pass

server.run()
