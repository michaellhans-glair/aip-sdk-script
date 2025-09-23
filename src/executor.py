"""
AIP Test Executor - Core execution logic for running test cases
"""

import csv
import json
import subprocess
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from .utils import thread_safe_print, Colors, sanitize_filename

logger = logging.getLogger(__name__)


class AIPTestExecutor:
    """Main class for executing AIP SDK test cases"""

    def __init__(
        self,
        test_cases_file="data/test_cases.csv",
        output_dir="output",
        specific_ids=None,
        combine_format_instructions=True,
    ):
        self.test_cases_file = test_cases_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.specific_ids = specific_ids
        self.combine_format_instructions = combine_format_instructions
        self.format_instructions = (
            self._load_format_instructions() if combine_format_instructions else ""
        )

    def _load_format_instructions(self):
        """Load format instructions from the format_instruction.txt file"""
        try:
            format_file = Path("instructions/format_instruction.txt")
            if format_file.exists():
                with open(format_file, "r", encoding="utf-8") as f:
                    return f.read().strip()
            else:
                logger.warning(
                    "Format instruction file not found at instructions/format_instruction.txt"
                )
                return ""
        except Exception as e:
            logger.error(f"Error loading format instructions: {e}")
            return ""

    def _combine_prompt_with_format_instructions(self, prompt):
        """Combine the user prompt with format instructions"""
        if self.combine_format_instructions and self.format_instructions:
            return f"{prompt}\n\n{self.format_instructions}"
        else:
            return prompt

    def read_test_cases(self):
        """Read test cases from CSV file"""
        test_cases = []
        try:
            with open(self.test_cases_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    test_case = {
                        "id": row["id"],
                        "agent_id": row["agent_id"],
                        "codename": row["codename"],
                        "prompt": row["prompt"],
                    }

                    # Filter by specific IDs if provided
                    if (
                        self.specific_ids is None
                        or test_case["id"] in self.specific_ids
                    ):
                        test_cases.append(test_case)

            if self.specific_ids:
                logger.info(
                    f"Loaded {len(test_cases)} test cases (filtered by IDs: {self.specific_ids}) from {self.test_cases_file}"
                )
            else:
                logger.info(
                    f"Loaded {len(test_cases)} test cases from {self.test_cases_file}"
                )
            return test_cases
        except FileNotFoundError:
            logger.error(f"Test cases file '{self.test_cases_file}' not found")
            return []
        except Exception as e:
            logger.error(f"Error reading test cases: {e}")
            return []

    def generate_output_filename(self, test_case):
        """Generate output filename based on test case"""
        id_part = test_case["id"]
        codename_part = sanitize_filename(test_case["codename"])
        query_part = sanitize_filename(test_case["prompt"])

        filename = f"{id_part}-{codename_part}-{query_part}.txt"
        return self.output_dir / filename

    def execute_agent(self, agent_id, prompt, test_case_id):
        """Execute agent with given prompt using AIP SDK"""
        try:
            # Combine prompt with format instructions
            combined_input = self._combine_prompt_with_format_instructions(prompt)

            # Use aip agents run command with --verbose flag
            cmd = [
                "aip",
                "agents",
                "run",
                agent_id,
                "--input",
                combined_input,
                "--verbose",
            ]

            logger.info(f"[ID {test_case_id}] Executing: {' '.join(cmd)}")

            # Run the command and capture output (no real-time display)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:
            logger.error(f"[ID {test_case_id}] Timeout executing agent {agent_id}")
            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timeout (5 minutes)",
                "return_code": -1,
            }
        except Exception as e:
            logger.error(f"[ID {test_case_id}] Error executing agent {agent_id}: {e}")
            return {"success": False, "stdout": "", "stderr": str(e), "return_code": -1}

    def save_result(self, test_case, execution_result, output_file):
        """Save execution result to output file"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Test Case ID: {test_case['id']}\n")
                f.write(f"Agent ID: {test_case['agent_id']}\n")
                f.write(f"Codename: {test_case['codename']}\n")
                f.write(f"Prompt: {test_case['prompt']}\n")
                f.write(f"Execution Time: {datetime.now().isoformat()}\n")
                f.write(f"Success: {execution_result['success']}\n")
                f.write(f"Return Code: {execution_result['return_code']}\n")
                f.write("-" * 50 + "\n")
                f.write("STDOUT:\n")
                f.write(execution_result["stdout"])
                f.write("\n" + "-" * 50 + "\n")
                f.write("STDERR:\n")
                f.write(execution_result["stderr"])
                f.write("\n" + "-" * 50 + "\n")

            logger.info(f"Result saved to: {output_file}")

        except Exception as e:
            logger.error(f"Error saving result to {output_file}: {e}")

    def run_test_case(self, test_case):
        """Run a single test case"""

        logger.info(f"Running test case {test_case['id']}: {test_case['codename']}")

        # Record start time
        start_time = datetime.now()

        # Execute the agent (always with --verbose flag for AIP SDK)
        execution_result = self.execute_agent(
            test_case["agent_id"], test_case["prompt"], test_case["id"]
        )

        # Record end time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        # Generate output filename
        output_file = self.generate_output_filename(test_case)

        # Save result
        self.save_result(test_case, execution_result, output_file)

        # Return success status and additional info
        return {
            "success": execution_result["success"],
            "execution_time": execution_time,
            "filename": str(output_file),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }

    def run_all_tests(self, max_workers=5):
        """Run all test cases in parallel"""
        test_cases = self.read_test_cases()

        if not test_cases:
            logger.error("No test cases to execute")
            return

        thread_safe_print(
            f"\n{Colors.BOLD}{Colors.CYAN}🚀 Starting PARALLEL execution of {len(test_cases)} test cases{Colors.END}"
        )
        thread_safe_print(
            f"{Colors.BOLD}{Colors.YELLOW}⚡ Running up to {max_workers} test cases simultaneously{Colors.END}"
        )
        thread_safe_print(
            f"{Colors.BOLD}{Colors.BLUE}📊 AIP agents will run with --verbose flag for detailed output{Colors.END}"
        )
        thread_safe_print()

        logger.info(
            f"Starting parallel execution of {len(test_cases)} test cases with {max_workers} workers"
        )

        results = {
            "total": len(test_cases),
            "successful": 0,
            "failed": 0,
            "details": [],
        }

        # Use ThreadPoolExecutor for parallel execution
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all test cases to the executor
            future_to_test = {
                executor.submit(self.run_test_case, test_case): test_case
                for test_case in test_cases
            }

            # Process completed test cases as they finish
            completed = 0
            for future in as_completed(future_to_test):
                test_case = future_to_test[future]
                completed += 1

                try:
                    result_info = future.result()
                    success = result_info["success"]

                    if success:
                        results["successful"] += 1
                        logger.info(
                            f"✓ Test case {test_case['id']} completed successfully"
                        )
                    else:
                        results["failed"] += 1
                        logger.warning(f"✗ Test case {test_case['id']} failed")

                    results["details"].append(
                        {
                            "id": test_case["id"],
                            "codename": test_case["codename"],
                            "query": test_case["prompt"],
                            "success": success,
                            "execution_time": result_info["execution_time"],
                            "filename": result_info["filename"],
                            "start_time": result_info["start_time"],
                            "end_time": result_info["end_time"],
                        }
                    )

                except Exception as e:
                    results["failed"] += 1
                    logger.error(
                        f"✗ Test case {test_case['id']} failed with exception: {e}"
                    )
                    results["details"].append(
                        {
                            "id": test_case["id"],
                            "codename": test_case["codename"],
                            "query": test_case["prompt"],
                            "success": False,
                            "error": str(e),
                            "execution_time": None,
                            "filename": None,
                            "start_time": None,
                            "end_time": None,
                        }
                    )

                # Show progress
                thread_safe_print(
                    f"{Colors.BOLD}{Colors.BLUE}📊 Progress: {completed}/{len(test_cases)} test cases completed{Colors.END}"
                )

        # Calculate additional statistics
        if results["details"]:
            execution_times = [
                detail["execution_time"]
                for detail in results["details"]
                if detail["execution_time"] is not None
            ]
            if execution_times:
                results["total_execution_time"] = sum(execution_times)
                results["average_execution_time"] = sum(execution_times) / len(
                    execution_times
                )
                results["min_execution_time"] = min(execution_times)
                results["max_execution_time"] = max(execution_times)
            else:
                results["total_execution_time"] = 0
                results["average_execution_time"] = 0
                results["min_execution_time"] = 0
                results["max_execution_time"] = 0

        # Save summary
        self.save_summary(results)

        thread_safe_print(
            f"\n{Colors.BOLD}{Colors.GREEN}🎉 PARALLEL execution completed: {results['successful']}/{results['total']} successful{Colors.END}"
        )
        logger.info(
            f"Parallel execution completed: {results['successful']}/{results['total']} successful"
        )
        return results

    def run_all_tests_sequential(self):
        """Run all test cases sequentially (original behavior)"""
        test_cases = self.read_test_cases()

        if not test_cases:
            logger.error("No test cases to execute")
            return

        thread_safe_print(
            f"\n{Colors.BOLD}{Colors.CYAN}🚀 Starting SEQUENTIAL execution of {len(test_cases)} test cases{Colors.END}"
        )
        logger.info(f"Starting sequential execution of {len(test_cases)} test cases")

        results = {
            "total": len(test_cases),
            "successful": 0,
            "failed": 0,
            "details": [],
        }

        for i, test_case in enumerate(test_cases, 1):
            try:
                thread_safe_print(
                    f"\n{Colors.BOLD}{Colors.BLUE}📊 Progress: {i}/{len(test_cases)}{Colors.END}"
                )
                result_info = self.run_test_case(test_case)
                success = result_info["success"]

                if success:
                    results["successful"] += 1
                    thread_safe_print(
                        f"{Colors.GREEN}✅ Test case {test_case['id']} completed successfully{Colors.END}"
                    )
                    logger.info(f"✓ Test case {test_case['id']} completed successfully")
                else:
                    results["failed"] += 1
                    thread_safe_print(
                        f"{Colors.RED}❌ Test case {test_case['id']} failed{Colors.END}"
                    )
                    logger.warning(f"✗ Test case {test_case['id']} failed")

                results["details"].append(
                    {
                        "id": test_case["id"],
                        "codename": test_case["codename"],
                        "query": test_case["prompt"],
                        "success": success,
                        "execution_time": result_info["execution_time"],
                        "filename": result_info["filename"],
                        "start_time": result_info["start_time"],
                        "end_time": result_info["end_time"],
                    }
                )

            except Exception as e:
                results["failed"] += 1
                thread_safe_print(
                    f"{Colors.RED}💥 Test case {test_case['id']} failed with exception: {e}{Colors.END}"
                )
                logger.error(
                    f"✗ Test case {test_case['id']} failed with exception: {e}"
                )
                results["details"].append(
                    {
                        "id": test_case["id"],
                        "codename": test_case["codename"],
                        "query": test_case["prompt"],
                        "success": False,
                        "error": str(e),
                        "execution_time": None,
                        "filename": None,
                        "start_time": None,
                        "end_time": None,
                    }
                )

        # Calculate additional statistics
        if results["details"]:
            execution_times = [
                detail["execution_time"]
                for detail in results["details"]
                if detail["execution_time"] is not None
            ]
            if execution_times:
                results["total_execution_time"] = sum(execution_times)
                results["average_execution_time"] = sum(execution_times) / len(
                    execution_times
                )
                results["min_execution_time"] = min(execution_times)
                results["max_execution_time"] = max(execution_times)
            else:
                results["total_execution_time"] = 0
                results["average_execution_time"] = 0
                results["min_execution_time"] = 0
                results["max_execution_time"] = 0

        # Save summary
        self.save_summary(results)

        thread_safe_print(
            f"\n{Colors.BOLD}{Colors.GREEN}🎉 SEQUENTIAL execution completed: {results['successful']}/{results['total']} successful{Colors.END}"
        )
        logger.info(
            f"Sequential execution completed: {results['successful']}/{results['total']} successful"
        )
        return results

    def save_summary(self, results):
        """Save execution summary"""
        summary_file = self.output_dir / "execution_summary.json"

        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            logger.info(f"Summary saved to: {summary_file}")

        except Exception as e:
            logger.error(f"Error saving summary: {e}")
