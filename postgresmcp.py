from fastmcp import FastMCP
import asyncpg
import os
import json
mcp = FastMCP("Postgres MCP")

@mcp.tool
async def test_tool(query: str) -> str:
    """Test the tool"""
    return "Test tool works abcd"
    


@mcp.tool
async def execute_query(query: str) -> str:
    """Execute a SQL query"""
    database_url = os.getenv("DATABASE_URL")
    # Strip asyncpg+ prefix if present (for SQLAlchemy compatibility)
    if database_url and database_url.startswith("asyncpg+"):
        database_url = database_url.replace("asyncpg+", "", 1)
    print(f"Connecting to: {database_url}")
    conn = await asyncpg.connect(database_url)
    try:
        if query.strip().upper().startswith("SELECT"):
            results = await conn.fetch(query)
            # Convert Record objects to dicts for JSON serialization
            results_list = [dict(record) for record in results]
            return json.dumps({"status": "success", "data": results_list})
        else:
            await conn.execute(query)
            conn.commit()
            return json.dumps({"status": "success", "message": "Query executed successfully"})
    except Exception as e:

        return json.dumps({"status": "error", "message": str(e)})
    finally:
        await conn.close()

if __name__ == "__main__":
    mcp.run(transport="stdio")