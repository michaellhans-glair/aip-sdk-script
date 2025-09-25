#!/usr/bin/env python3
"""
AIP SDK Test Case Executor

This script reads test cases from a CSV file, executes them using the AIP SDK,
and saves the results to output files with the naming convention: id-codename-query
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils import setup_logging
from src.cli import parse_arguments
from src.executor import AIPTestExecutor
from src.display import display_execution_summary, log_execution_info


def main():
    """Main entry point for the AIP SDK Test Script"""
    # Setup logging
    setup_logging()

    # Parse command line arguments
    args = parse_arguments()
    if args is None:  # List command was executed
        return

    # Log execution information
    log_execution_info(args)

    # Create executor and run tests
    combine_format = (
        not args.no_format
    )  # Default is True, unless --no-format is specified
    executor = AIPTestExecutor(
        args.test_cases, args.output, args.specific_ids, combine_format
    )

    if args.sequential:
        # Run sequentially
        results = executor.run_all_tests_sequential()
    else:
        # Run in parallel
        results = executor.run_all_tests(args.workers)

    # Display results
    display_execution_summary(results, args.output, getattr(args, "prod", False))


if __name__ == "__main__":
    main()
