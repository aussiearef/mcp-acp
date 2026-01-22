from fastmcp import FastMCP

mcp = FastMCP("My App")

# Static resource. Is discovered by resources/list
@mcp.resource("config://app", name="Config", title="Application Configuration")
def get_config() -> str:
    return "App configuration here"

# Dynamic resource. Is discovered by resources/templates/list
@mcp.resource("users://{user_id}/profile", name="User Profile", title="User Profile")
def get_user_profile(user_id: str) -> str:
    return f"Profile data for user {user_id}"