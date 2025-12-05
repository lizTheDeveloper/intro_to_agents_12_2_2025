from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

current_dir = Path(__file__).parent
samples_dir = current_dir / "recipes"
cooking_agent_system_instructions = open(samples_dir / "cooklang_styleguide.md").read()

async def main(user_request):
    async with MCPServerStdio(
        name="Filesystem Server via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
        },
    ) as server:
        async with MCPServerStdio(
            name="Postgres MCP",
            params={
                "command": "/Users/annhoward/intro_to_agents_12_2_2025/env/bin/python",
                "args": ["postgresmcp.py"],
                "env": {
                    "DATABASE_URL": os.getenv("DATABASE_URL"),
                    "PATH": os.getenv("PATH", ""),
                },
            },
        ) as postgres_server:
            agent = Agent(
                name="Recipe Extraction Agent",
                instructions=cooking_agent_system_instructions,
                mcp_servers=[server, postgres_server],
            )
            result = await Runner.run(agent, user_request)
            print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main("Create tables for storing recipes and, I don't know, making collections of recipes and things like that, tags, whatever you might need. Just set up your database. I don't see the tables, so please ensure they are really there."))