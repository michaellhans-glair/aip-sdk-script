import csv
import sys
import os

from glaip_sdk import Client
from dotenv import load_dotenv

load_dotenv()


def select_agent(agents_csv):
    """
    Display a list of available agents from the given CSV file and prompt the user to select one.

    Args:
        agents_csv (str): Path to the agents CSV file.

    Returns:
        dict: The selected agent's information as a dictionary.
    """
    agents = []
    with open(agents_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            agents.append(row)
    print("Available agents:")
    for idx, agent in enumerate(agents):
        print(f"{idx+1}. {agent['name']} (ID: {agent['id']})")
    while True:
        try:
            choice = int(input("Select agent by number: "))
            if 1 <= choice <= len(agents):
                return agents[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def read_instruction_file(filename):
    """
    Read and return the contents of the specified instruction file.

    Args:
        filename (str): Path to the instruction file.

    Returns:
        str: Contents of the instruction file.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def main():
    """
    Main entry point for updating an AIP agent using the Python SDK.

    This script allows the user to:
      - Select an agent from a CSV file.
      - Specify an instruction file to update the agent's instructions.
      - Optionally provide a new name for the agent.
      - Retrieve the agent's current details (including mcps).
      - Update the agent using the Python SDK, passing the mcps attribute.
    """
    # Initialize the AIP SDK client (loads environment variables)
    client = Client()

    agents_csv = "data/agents.csv"
    agent = select_agent(agents_csv)
    print(f"Selected agent: {agent['name']} (ID: {agent['id']})")

    # Retrieve agent details (including mcps) using the SDK
    try:
        agent_obj = client.get_agent_by_id(agent["id"])
    except Exception as e:
        print(f"Failed to retrieve agent details: {e}")
        sys.exit(1)

    # Try to get mcps from agent object
    mcps = getattr(agent_obj, "mcps", None)
    if mcps is None:
        print(
            "Warning: 'mcps' attribute not found in agent details. Proceeding with mcps=None."
        )

    instruction_filename = input(
        "Enter instruction filename (e.g., gmail.txt): "
    ).strip()
    instruction_file = os.path.join("instructions", instruction_filename)
    try:
        instruction = read_instruction_file(instruction_file)
    except Exception as e:
        print(f"Failed to read instruction file: {e}")
        sys.exit(1)
    new_name = input(
        f"Enter new agent name (leave blank to keep '{agent['name']}'): "
    ).strip()

    # Prepare the list of MCP IDs if present
    mcps_ids = None
    if mcps is not None:
        if isinstance(mcps, list):
            mcps_ids = []
            for mcp in mcps:
                if isinstance(mcp, dict) and "id" in mcp:
                    mcps_ids.append(mcp["id"])
                elif isinstance(mcp, str):
                    mcps_ids.append(mcp)
        else:
            print("Warning: 'mcps' attribute is not a list. Skipping mcps argument.")

    # Prepare update kwargs
    update_kwargs = {"instruction": instruction}
    if mcps_ids is not None:
        update_kwargs["mcps"] = mcps_ids
    if new_name:
        update_kwargs["name"] = new_name

    print(
        f"Updating agent '{agent['name']}' (ID: {agent['id']}) with the following parameters:"
    )
    for k, v in update_kwargs.items():
        if k == "instruction":
            print(f"  {k}: <instruction text of length {len(v)}>")
        else:
            print(f"  {k}: {v}")

    try:
        updated_agent = client.update_agent(agent["id"], **update_kwargs)
        print("Agent updated successfully.")
        print("Updated agent details:")
        print(updated_agent)
    except Exception as e:
        print(f"Failed to update agent: {e}")


if __name__ == "__main__":
    main()
