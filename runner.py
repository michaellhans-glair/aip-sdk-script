"""
Simple GLAIP SDK Runner

A straightforward script that directly uses the GLAIP SDK to run agent queries.

Input:
    - query: The search query
    - bosa_token: BOSA authentication token
    - agent_id: The agent ID (UUID)
    - aip_api_url: AIP API base URL
    - aip_api_key: AIP API key
    - bosa_api_key: BOSA API key (optional, for MCP authentication)

Output:
    Streaming responses in beautified format
"""

import asyncio
import json
from glaip_sdk.client.agents import AgentClient
import os
from dotenv import load_dotenv

load_dotenv()

def print_raw_response(data: dict) -> None:
    """Print raw response data in a box."""
    print("\n" + "─" * 80)
    print(json.dumps(data, indent=2))
    print("─" * 80)


async def main():
    """Main function to run GLAIP agent query."""
    # Direct configuration - modify these values
    query = "List all my upcoming meetings today"
    agent_id = "d7391163-9ac9-4026-98aa-c1b8b138fe8a"
    aip_api_url = os.getenv("AIP_API_URL")
    aip_api_key = os.getenv("AIP_API_KEY")
    bosa_token = os.getenv("BOSA_USER_TOKEN")
    bosa_api_key = os.getenv("BOSA_API_KEY")
    
    try:
        # Initialize GLAIP SDK client
        client = AgentClient(api_url=aip_api_url, api_key=aip_api_key)
        
        # Get agent configuration to retrieve tool_ids and mcp_ids
        agent_config = client.get_agent_by_id(agent_id=agent_id)
        tool_ids = [tool["id"] for tool in agent_config.tools]
        mcp_ids = [mcp["id"] for mcp in agent_config.mcps]
        
        # Build payload
        payload = {
            "input": query,
        }
        
        # Add authentication configs if BOSA token is provided
        if bosa_token:
            # Tool configs: map each tool_id to bosa_token
            tool_configs = {tool_id: {"bosa_token": bosa_token} for tool_id in tool_ids}
            payload["tool_configs"] = tool_configs
            
            # MCP configs: map each mcp_id to authentication headers
            if bosa_api_key:
                mcp_configs = {
                    mcp_id: {
                        "authentication": {
                            "type": "custom-header",
                            "headers": {
                                "X-Api-Key": bosa_api_key,
                                "Authorization": f"Bearer {bosa_token}",
                            },
                        }
                    }
                    for mcp_id in mcp_ids
                }
                payload["mcp_configs"] = mcp_configs
        
        # Run agent with streaming
        print(json.dumps(payload, indent=2))
        response = client.arun_agent(
            agent_id=agent_id,
            message=payload.pop("input", ""),
            timeout=500,
            **payload
        )
        
        # Process streaming response
        async for data in response:
            print_raw_response(data)
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
