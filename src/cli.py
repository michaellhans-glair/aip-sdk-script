"""
Command Line Interface for AIP SDK Test Script
"""

import argparse
import csv
from .utils import parse_id_list


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(description="Execute AIP SDK test cases from CSV")
    parser.add_argument(
        "--test-cases",
        "-t",
        default="data/test_cases.csv",
        help="Path to test cases CSV file (default: data/test_cases.csv)",
    )
    parser.add_argument(
        "--output", "-o", default="output", help="Output directory (default: output)"
    )
    parser.add_argument(
        "--ids",
        "-i",
        help='Specific test case IDs to run (comma-separated or ranges, e.g., "1,3,5-8")',
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available test case IDs and exit",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=5,
        help="Number of parallel workers (default: 5)",
    )
    parser.add_argument(
        "--sequential",
        "-s",
        action="store_true",
        help="Run test cases sequentially instead of in parallel",
    )
    parser.add_argument(
        "--no-format",
        action="store_true",
        help="Disable automatic inclusion of format instructions with prompts",
    )
    parser.add_argument(
        "--prod",
        action="store_true",
        help="Use production test cases and agents (data/test_cases_prod.csv)",
    )

    return parser


def handle_list_command(args):
    """Handle the --list command to show available test cases"""
    try:
        with open(args.test_cases, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            print("Available test case IDs:")
            for row in reader:
                print(
                    f"  ID: {row['id']} - {row['codename']} - {row['prompt'][:50]}..."
                )
    except FileNotFoundError:
        print(f"Test cases file '{args.test_cases}' not found")


def parse_arguments():
    """Parse command line arguments and return parsed args"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle production flag
    if args.prod:
        args.test_cases = "data/test_cases_prod.csv"

    # Handle list command
    if args.list:
        handle_list_command(args)
        return None

    # Parse specific IDs if provided
    args.specific_ids = parse_id_list(args.ids)

    return args
