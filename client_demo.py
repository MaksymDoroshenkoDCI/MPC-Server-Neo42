import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_demo():
    # Configure the server parameters
    # We point to the python executable in our venv and the server.py script
    server_params = StdioServerParameters(
        command="venv/bin/python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            print("\n--- MCP Client Demo: Querying Neo42 APC ---\n")

            # 1. Search for packages
            print("Action: Searching for 'Chrome'...")
            result = await session.call_tool("search_packages", arguments={"query": "Chrome"})
            print(f"Result: {result.content[0].text}\n")

            # 2. Get deployment status for a failed package
            print("Action: Checking status of 'Neo42 Service Agent' on 'WS-DEV-MAX'...")
            result = await session.call_tool("get_package_status", arguments={
                "package_name": "Neo42 Service Agent",
                "hostname": "WS-DEV-MAX"
            })
            print(f"Result: {result.content[0].text}\n")

            # 3. List inventory for a specific server
            print("Action: Listing inventory for 'SRV-PROD-01'...")
            result = await session.call_tool("list_server_inventory", arguments={"hostname": "SRV-PROD-01"})
            print(f"Result: {result.content[0].text}\n")

            # 4. Check rental availability
            print("Action: Checking availability of 'Notebooks'...")
            result = await session.call_tool("check_rental_availability", arguments={"asset_type": "Notebook"})
            print(f"Result: {result.content[0].text}\n")

            # 5. Get recent pipelines
            print("Action: Fetching recent pipelines...")
            result = await session.call_tool("get_recent_pipelines", arguments={})
            print(f"Result: {result.content[0].text}\n")

if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except Exception as e:
        print(f"Error: {e}")
