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

```
🚀 Starting PARALLEL execution of 12 test cases
⚡ Running up to 5 test cases simultaneously

📊 Progress: 1/12 test cases completed
📊 Progress: 2/12 test cases completed
...
📊 Progress: 12/12 test cases completed

🎉 PARALLEL execution completed: 10/12 successful

============================================================
📊 EXECUTION SUMMARY 📊
============================================================
📈 Total test cases: 12
✅ Successful: 10
❌ Failed: 2
📊 Success rate: 83.3%
============================================================
```

## Requirements

- Python 3.7+
- AIP SDK installed and configured
- Valid agent IDs in your CSV file

## Troubleshooting

- **Agent not found**: Verify agent IDs in your CSV file
- **Permission errors**: Check write access to output directory
- **Timeout errors**: Some agents may take longer than 5 minutes
- **CSV format issues**: Ensure proper comma-separated formatting

For detailed logs, check `test_execution.log`.

## GL AIP SDK Guide
For more references, please refer to this [link](https://gdplabs.gitbook.io/ai-agents-platform/gl-aip-sdk/get-started/quick-start)