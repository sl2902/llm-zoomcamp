#!/usr/bin/env python3
"""
FastMCP Client - Much simpler than manual JSON-RPC!
"""
import asyncio
from fastmcp import Client

async def main():
    # Option 1: If running as a script, use the server file path
    async with Client("weather_server.py") as mcp_client:
        print("=== Connected to MCP Server ===")
        
        # Get list of available tools
        print("\n=== Getting list of tools ===")
        tools = await mcp_client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call get_weather for Berlin
        print("\n=== Getting weather for Berlin ===")
        berlin_weather = await mcp_client.call_tool("get_weather", {"city": "Berlin"})
        print(f"Berlin weather: {berlin_weather}")
        
        # Set weather for Paris
        print("\n=== Setting weather for Paris to 22.5°C ===")
        set_result = await mcp_client.call_tool("set_weather", {"city": "Paris", "temp": 22.5})
        print(f"Set weather result: {set_result}")
        
        # Get weather for Paris (should return 22.5)
        print("\n=== Getting weather for Paris ===")
        paris_weather = await mcp_client.call_tool("get_weather", {"city": "Paris"})
        print(f"Paris weather: {paris_weather}")

# Alternative version for Jupyter notebooks
async def main_jupyter():
    # First import your weather server module
    import weather_server
    
    # Option 2: If running in Jupyter, pass the mcp instance directly
    async with Client(weather_server.mcp) as mcp_client:
        print("=== Connected to MCP Server (Jupyter) ===")
        
        # Get list of available tools
        print("\n=== Getting list of tools ===")
        tools = await mcp_client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call get_weather for Tokyo
        print("\n=== Getting weather for Tokyo ===")
        tokyo_weather = await mcp_client.call_tool("get_weather", {"city": "Tokyo"})
        print(f"Tokyo weather: {tokyo_weather}")

if __name__ == "__main__":
    # For running as a script
    print("Running FastMCP Client...")
    asyncio.run(main())