from mcp.server.fastmcp import FastMCP , Context 
from fastmcp.server.dependencies import get_http_headers
from pydantic import BaseModel
import asyncio
from authlib.jose import JWTClaims , JsonWebToken # pip install  authlib

mcp = FastMCP(stateless_http=True)

class Greeting(BaseModel):
    message: str

@mcp.tool("Greetings")
def greetings (name:str , ctx: Context) -> Greeting:
    """A tool function that accepts a parameter called name and returns a personalised greeting message."""

    #   BEGIN AUTH
    headers = get_http_headers()  # Access headers from ctx.request
    authorization_header = headers["Authorization"]
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.replace("Bearer ", "", 1)
        with open("./public.pem", "r", encoding="utf-8") as f:
            public_key = f.read()
            token =JsonWebToken(algorithms="RS256")
            claims: JWTClaims = token.decode(token, public_key)

            token_name = claims["name"]
    #   END AUTH

    return  Greeting(message= f"Special greetings to, {token_name}")

async def main():
   
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())