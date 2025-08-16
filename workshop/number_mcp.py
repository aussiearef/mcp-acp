# MCP tool to get the status of a mobile number (in Australian format)
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import asyncio
import sqlite3

class Status(BaseModel):
    status: str = "not_found"
    number: str = ""
    

app = FastMCP(name="get-sim-status-mcp", host="0.0.0.0", port=8000)

conn = sqlite3.connect("mcp-acp.db")
cursor = conn.cursor()


@app.tool(name="get_number_status", description="Gets a SIM card's (of a mobile number) status by SIM or mobile number")
async def get_number_status(number: str) -> Status:
    cursor.execute("SELECT status FROM numbers WHERE number = ?", (number,))
    row = cursor.fetchone()
    result = Status(number=number)
    
    if row:
       result.status = row[0] 
    else:
        result.status="not_found"
        
    return result

@app.tool(name="set_number_status", description="Sets a SIM card's (of a mobile number) status by SIM or mobile number.")
async def set_number_status(number: str, new_status: str) -> Status:
    cursor.execute("UPDATE numbers set status=? WHERE number = ?", (new_status, number))
    conn.commit()
    result = Status(number=number)
    if cursor.rowcount > 0:
        result.status = new_status
    else:
        result.status = "not_found"

    return result
    
        

async def main():
    await app.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())
