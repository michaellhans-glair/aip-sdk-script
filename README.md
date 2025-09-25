# AIP SDK Test Script

Execute multiple AIP SDK agent test cases in parallel from a CSV file with progress tracking and detailed results.

## Features

- 🚀 **Parallel Execution**: Run up to 5 test cases simultaneously
- 📊 **Progress Tracking**: Real-time progress updates
- 📁 **Organized Output**: Results saved with descriptive filenames
- 🎯 **Selective Testing**: Run specific test case IDs or ranges
- 🎨 **Colorful Output**: Easy-to-read terminal output
- 🔄 **Environment Support**: Separate development and production testing
- 🏷️ **Codename-based**: Use friendly codenames instead of agent IDs

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
   id,codename,prompt
   1,gmail,Find emails with subject containing 'Project report'
   2,gdrive,Find documents related to "Deep Research"
   ```

   **Create agents file** (`data/agents.csv`):
   ```csv
   id,name,codename,type,framework,version
   9c0ae488-4d87-4b5c-a91f-5d3b255b2c02,"[SS v2] Github Agent",github,config,langchain,1.0.0
   a6555bea-7860-4c06-bbf8-4be3030534e6,"[SS v2 Prod] Google Mail Agent",gmail-prod,config,langchain,1.0.0
   ```

3. **Setup the GL AIP SDK** using the command below:
   ```bash
   aip init
   ```

4. **Run tests:**
   ```bash
   # Run all test cases (development mode)
   python main.py

   # Run production test cases
   python main.py --prod

   # Run specific IDs
   python main.py --ids "1,3,5"

   # Run production tests with specific IDs
   python main.py --prod --ids "1,3,5"

   # Run with 3 workers
   python main.py --workers 3

   # List available test cases
   python main.py --list

   # List production test cases
   python main.py --prod --list
   ```
   Or, using `make`:
   ```bash
   # Run all development test cases
   make run

   # Run all production test cases
   make run-prod

   # Run specific IDs (development)
   make run ARGS="--ids \"1,3,5\""

   # Run specific IDs (production)
   make run-prod ARGS="--ids \"1,3,5\""

   # Run with 3 workers
   make run ARGS="--workers 3"

   # Run production tests sequentially
   make run-prod ARGS="--sequential"

   # List development test cases
   make list

   # List production test cases
   make list-prod

   # Show all available make targets
   make help
   ```

## Environment Modes

The script supports two environment modes:

### Development Mode (Default)
- Uses `data/test_cases.csv` and development agents
- Agent codenames: `github`, `gmail`, `gdrive`, `gcalendar`, `chief`
- Safe for testing and development

### Production Mode (`--prod` flag)
- Uses `data/test_cases_prod.csv` and production agents
- Agent codenames: `github-prod`, `gmail-prod`, `gdrive-prod`, `gcalendar-prod`, `chief-prod`
- For production environment testing

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
| `--prod` | Use production test cases and agents | Development mode |
| `--no-format` | Disable automatic format instructions | Format instructions enabled |

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
