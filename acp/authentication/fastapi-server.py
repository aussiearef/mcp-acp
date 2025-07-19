from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from acp_sdk.server import Server, Context
from acp_sdk.models import Message

server = Server()
security = HTTPBearer()

VALID_TOKEN = "your-secret-token" # read from a secret manager

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token",
        )
    return "authenticated-user"

@server.agent("myagent")
async def myagent(input : Message = Depends(authenticate),
                  context: Context = None):
    pass

server.run()








