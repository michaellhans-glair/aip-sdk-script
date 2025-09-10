# AIP SDK Test Script

Execute multiple AIP SDK agent test cases in parallel from a CSV file with progress tracking and detailed results.

## Features

- 🚀 **Parallel Execution**: Run up to 5 test cases simultaneously
- 📊 **Progress Tracking**: Real-time progress updates
- 📁 **Organized Output**: Results saved with descriptive filenames
- 🎯 **Selective Testing**: Run specific test case IDs or ranges
- 🎨 **Colorful Output**: Easy-to-read terminal output

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or, using `make`:
   ```bash
   make install
   ```

2. **Create test cases file** (`data/test_cases.csv`):
   ```csv
   id,agent_id,codename,prompt
   1,ecca3133-e89a-49e2-8e77-03a68d13c648,gmail,Find emails with subject containing 'Project report'
   2,6907666c-1be2-46ba-86fa-79f24d66348a,gdrive,Find documents related to "Deep Research"
   ```

3. **Setup the GL AIP SDK** using the command below:
   ```bash
   aip init
   ```

4. **Run tests:**
   ```bash
   # Run all test cases
   python main.py

   # Run specific IDs
   python main.py --ids "1,3,5"

   # Run with 3 workers
   python main.py --workers 3

   # List available test cases
   python main.py --list
   ```
   Or, using `make run`:
   ```bash
   # Run all test cases
   make run

   # Run specific IDs
   make run ARGS="--ids \"1,3,5\""

   # Run with 3 workers
   make run ARGS="--workers 3"

   # List available test cases
   make run ARGS="--list"
   ```

5. **Update agent list from source (optional):**
   ```bash
   # This will update data/agents.csv with the latest agent info
   python update.py
   ```

   Or, if using `make`:
   ```bash
   make update
   ```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--test-cases`, `-t` | Path to test cases CSV file | `data/test_cases.csv` |
| `--output`, `-o` | Output directory | `output` |
| `--ids`, `-i` | Specific test case IDs to run | All test cases |
| `--workers`, `-w` | Number of parallel workers | `5` |
| `--sequential`, `-s` | Run sequentially instead of parallel | Parallel mode |
| `--list`, `-l` | List available test cases and exit | - |

## Output

- **Result files**: `{id}-{codename}-{query}.txt` in the output directory
- **Summary**: `execution_summary.json` with statistics
- **Logs**: `test_execution.log` with detailed execution logs

## Example Output
