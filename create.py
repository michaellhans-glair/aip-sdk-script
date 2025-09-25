"""
Script to create multiple agents using the glaip_sdk Client.

This script loads environment variables for API configuration, reads agent instructions
from text files, and creates a set of predefined agents with associated tools and MCPs.

Environment Variables:
    AIP_BASE_URL: The base URL for the AIP API.
    AIP_API_KEY: The API key for authentication.

Instructions for each agent are expected to be present in the 'instructions/' directory,
with filenames matching the agent's function (e.g., 'github.txt', 'gcalendar.txt', etc.).

Agents created:
    - [SS v2] Github Agent
    - [SS v2] Google Calendar Agent
    - [SS v2] Google Mail Agent
    - [SS v2] Google Drive Agent

Each agent is created with a shared tool and a specific MCP.

Usage:
    python create.py
"""

import os
from glaip_sdk import Client
from dotenv import load_dotenv

load_dotenv()

AIP_BASE_URL = os.getenv("AIP_API_URL")
AIP_API_KEY = os.getenv("AIP_API_KEY")


tool_id = "18777d0f-5fd3-4570-a282-bc3c18333e0b"

mcp_github_id = "90d0788a-53e9-4953-9c13-0fca1c0eafc2"
mcp_google_calendar_id = "9520c4e2-ccb7-40aa-8925-5275185c18a0"
mcp_google_mail_id = "62dff95e-5f3a-4890-a9c7-b83f1455db74"
mcp_google_drive_id = "fc4ef652-a14f-4b91-b05c-804bdbc13fa8"

github_agent_id = "207efb4c-c9fc-4ad1-8efc-583caabdaca2"
google_calendar_agent_id = "21e0d485-b971-4768-94e0-d145dd1483f0"
google_mail_agent_id = "a6555bea-7860-4c06-bbf8-4be3030534e6"
google_drive_agent_id = "9183b415-7de1-4bc2-8b68-d1f00cb19b2b"


def get_agent_instruction(name):
    """
    Read and return the instruction text for a given agent.

    Args:
        name (str): The name of the agent instruction file (without extension).

    Returns:
        str: The instruction text.
    """
    with open(f"instructions/{name}.txt", "r") as f:
        return f.read().strip()


agents = [
    {
        "name": "[SS v2] Github Agent",
        "instruction": get_agent_instruction("github"),
        "tools": [tool_id],
        "mcps": [mcp_github_id],
    },
    {
        "name": "[SS v2] Google Calendar Agent",
        "instruction": get_agent_instruction("gcalendar"),
        "tools": [tool_id],
        "mcps": [mcp_google_calendar_id],
    },
    {
        "name": "[SS v2] Google Mail Agent",
        "instruction": get_agent_instruction("gmail"),
        "tools": [tool_id],
        "mcps": [mcp_google_mail_id],
    },
    {
        "name": "[SS v2] Google Drive Agent",
        "instruction": get_agent_instruction("gdrive"),
        "tools": [tool_id],
        "mcps": [mcp_google_drive_id],
    },
    {
        "name": "[SS v2] Chief Retrieval Agent",
        "instruction": get_agent_instruction("chief"),
        "tools": [tool_id],
        "agents": [
            github_agent_id,
            google_calendar_agent_id,
            google_mail_agent_id,
            google_drive_agent_id,
        ],
    },
]


def main():
    """
    Create agents as defined in the 'agents' list using the glaip_sdk Client.
    Prints the name and ID of each created agent.
    """
    client = Client(api_url=AIP_BASE_URL, api_key=AIP_API_KEY)

    for agent in agents:
        try:
            created_agent = client.create_agent(**agent)
            print(
                f"Created agent: {created_agent.name} (ID: {getattr(created_agent, 'id', 'N/A')})"
            )
        except Exception as e:
            print(f"Failed to create agent '{agent.get('name', 'Unknown')}': {e}")


def delete_agents():
    """
    Delete an agent using the glaip_sdk Client.
    """
    client = Client(api_url=AIP_BASE_URL, api_key=AIP_API_KEY)

    agent_ids = [
        "14b37242-409f-4aff-a6e1-9b6d904f2f25",
        "fc8ffa77-997f-40a5-8873-cf38620ad7b3",
        "f85ccd1a-f3f4-4d56-b064-2f72f4a6fbe1",
        "8fc64c12-c6cc-4815-908a-79633f0e4682",
        "795f0e50-92d6-4281-9bb1-e21fc38d93f8",
    ]
    for aid in agent_ids:
        client.delete_agent(aid)
        print(f"Deleted agent: {aid}")


if __name__ == "__main__":
    delete_agents()
    # main()
