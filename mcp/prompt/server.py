from fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP()

@mcp.prompt(title="Attention Prompt", description="This prompt is used to draw attention to a specific message.")
async def show_prompt(message:str) ->str:
    return f"Please pay attention to {message}"


@mcp.prompt(title="Debug Code", description="This prompt is used to debug code snippets.")
async def debug_code(code: str) -> list[base.Message]:
   return [
       base.UserMessage("I can see this code has errors."),
       base.AssistantMessage("What have you tried so far?")
   ]