"""
Simple GLAIP SDK Runner

A straightforward script that uses the AIPRunner module to run agent queries.

Input:
    - query: The search query
    - agent_id: The agent ID (UUID)
    - Environment variables: AIP_API_URL, AIP_API_KEY, BOSA_USER_TOKEN, BOSA_API_KEY

Output:
    Streaming responses in beautified format
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.runner import AIPRunner, print_raw_response


async def main():
    """Main function to run GLAIP agent query."""
    # Direct configuration - modify these values
    query = "List all my upcoming meetings today"
    agent_id = "d7391163-9ac9-4026-98aa-c1b8b138fe8a"

    try:
        # Initialize runner
        runner = AIPRunner()

        # Run agent with streaming
        print(f"Running agent {agent_id} with query: {query}")
        async for data in runner.run_agent_streaming(agent_id, query):
            print_raw_response(data)

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
