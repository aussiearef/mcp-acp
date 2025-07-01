from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP()

class Greeting(BaseModel):
    message: str

@mcp.tool("Greetings")
def greetings (name:str) -> Greeting:
    """A tool function that accepts a paratamer called name and returns a personalised greeting message."""
    return  Greeting(message= "Hello, {name}")