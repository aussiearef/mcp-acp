# MCP tool to get the status of a mobile number (in Australian format)
from mcp.server.fastmcp import FastMCP 
from pydantic import BaseModel
import asyncio
import sqlite3
import os

# Below classes are imported to add a middleware to starlett app , so it intercepts http request and check x-api-key header.
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class Status(BaseModel):
    status: str = "not_found"
    number: str = ""

app = FastMCP(name="get-sim-status-mcp", host="0.0.0.0", port=8000,)



@app.tool(name="get_number_status", description="Gets a SIM card's (of a mobile number) status by SIM or mobile number")
async def get_number_status(number: str) -> Status:

    conn = sqlite3.connect("mcp-a2a.db" , check_same_thread=False)
    cursor = conn.cursor()
    result = Status(number=number)

    try:
        cursor.execute("SELECT status FROM numbers WHERE number = ?", (number,))
        row = cursor.fetchone()
        if row:
            result.status = row[0] 
        else:
             result.status="not_found"
    except ValueError as e:
        result.status=str(e)
    cursor.close()  
    return result

@app.tool(name="set_number_status", description="Sets a SIM card's (of a mobile number) status by SIM or mobile number.")
async def set_number_status(number: str, new_status: str  ) -> Status:
    result = Status(number=number)

    print("set_number_status")
    conn = sqlite3.connect("mcp-a2a.db" , check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE numbers set status=? WHERE number = ?", (new_status, number))
    conn.commit()

    if cursor.rowcount > 0:
        result.status = new_status
    else:
        result.status = "not_found"
    cursor.close()
    return result
    
           
class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Read the body
        body = await request.body()
        if body:
            print(f"DEBUG MCP Body: {body.decode()}")

        # Re-wrap the request so the next handler can read the body again
        async def receive():
            return {"type": "http.request", "body": body}

        new_request = Request(request.scope, receive=receive)
        
        provided_key = request.headers.get("x-api-key")
        expected_key = os.environ.get("mcp_api_key", "123")

        if provided_key != expected_key:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)

        return await call_next(new_request)


async def main():
    import uvicorn

    starlette_app = app.streamable_http_app()
    starlette_app.add_middleware(APIKeyMiddleware)
    config = uvicorn.Config(
        starlette_app,
        host="0.0.0.0",
        port=8000
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
