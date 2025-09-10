import csv
import subprocess
import sys
import os


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
    Main entry point for updating an AIP agent.

    This script allows the user to:
      - Select an agent from a CSV file.
      - Specify an instruction file to update the agent's instructions.
      - Optionally provide a new name for the agent.
      - Run the 'aip agents update' command to update the agent.
    """
    agents_csv = "data/agents.csv"
    agent = select_agent(agents_csv)
    print(f"Selected agent: {agent['name']} (ID: {agent['id']})")
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
    cmd = ["aip", "agents", "update", agent["id"], "--instruction", instruction]
    if new_name:
        cmd.extend(["--name", new_name])
    print(f"Running: {' '.join(cmd[:4])} ...")
    try:
        result = subprocess.run(cmd, input=instruction, text=True, capture_output=True)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        if result.returncode == 0:
            print("Agent updated successfully.")
        else:
            print(f"Failed to update agent. Exit code: {result.returncode}")
    except Exception as e:
        print(f"Error running aip command: {e}")


if __name__ == "__main__":
    main()
