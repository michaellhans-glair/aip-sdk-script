# AIP SDK Test Script

A Python script for executing multiple AIP SDK agent test cases in parallel from a CSV file. This tool allows you to run batch tests against your AI agents efficiently with progress tracking and detailed result logging.

## Features

- 🚀 **Parallel Execution**: Run up to 5 test cases simultaneously (configurable)
- 📊 **Progress Tracking**: Real-time progress updates during execution
- 📁 **Organized Output**: Results saved with descriptive filenames
- 🎯 **Selective Testing**: Run specific test case IDs or ranges
- 📝 **Comprehensive Logging**: Detailed logs and execution summaries
- 🔄 **Flexible Execution**: Sequential or parallel modes
- 🎨 **Colorful Output**: Easy-to-read terminal output with colors

## Prerequisites

- Python 3.7+
- AIP SDK installed and configured
- Valid agent IDs and test cases

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## File Structure

```
aip-sdk-script/
├── main.py              # Main script
├── test_cases.csv       # Test cases configuration
├── agents.csv          # Agent information
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── output/            # Generated results (created automatically)
│   ├── execution_summary.json
│   └── [test-case-results].txt
└── test_execution.log # Execution log file
```

## Configuration

### Test Cases CSV Format

Create a `test_cases.csv` file with the following columns:

```csv
id,agent_id,codename,prompt
1,ecca3133-e89a-49e2-8e77-03a68d13c648,gmail,Find emails with subject containing 'Project report'
2,ecca3133-e89a-49e2-8e77-03a68d13c648,gmail,Find emails mentioning 'Weekly report'
3,6907666c-1be2-46ba-86fa-79f24d66348a,gdrive,Find documents related to "Deep Research"
```

**Columns:**
- `id`: Unique identifier for the test case
- `agent_id`: AIP SDK agent ID to execute
- `codename`: Short name for the test case
- `prompt`: The input prompt to send to the agent

### Agents CSV Format

Create an `agents.csv` file with agent information:

```csv
id,name,type,framework,version
ecca3133-e89a-49e2-8e77-03a68d13c648,"[SS] Google Mail Agent",config,langchain,1.0.0
6907666c-1be2-46ba-86fa-79f24d66348a,"[SS] Google Drive Agent",config,langchain,1.0.0
```

## Usage

### Basic Usage

```bash
# Run all test cases with default settings (5 parallel workers)
python main.py

# Run with custom number of workers
python main.py --workers 3

# Run specific test case IDs
python main.py --ids "1,3,5"

# Run a range of test case IDs
python main.py --ids "1-5"

# Run mixed IDs and ranges
python main.py --ids "1,3,5-8,10"
```

### Advanced Options

```bash
# Use custom test cases file
python main.py --test-cases my_tests.csv

# Use custom output directory
python main.py --output results

# Run sequentially instead of parallel
python main.py --sequential

# List available test cases without running
python main.py --list
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--test-cases` | `-t` | Path to test cases CSV file | `test_cases.csv` |
| `--output` | `-o` | Output directory for results | `output` |
| `--ids` | `-i` | Specific test case IDs to run | All test cases |
| `--workers` | `-w` | Number of parallel workers | `5` |
| `--sequential` | `-s` | Run test cases sequentially | Parallel mode |
| `--list` | `-l` | List available test cases and exit | - |

## Examples

### Example 1: Run All Test Cases

```bash
python main.py
```

**Output:**
```
🚀 Starting PARALLEL execution of 12 test cases
⚡ Running up to 5 test cases simultaneously
📊 AIP agents will run with --verbose flag for detailed output

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

📁 Results saved in: output/
📝 Log file: test_execution.log
============================================================
```

### Example 2: Run Specific Test Cases

```bash
python main.py --ids "1-5" --workers 3
```

### Example 3: List Available Test Cases

```bash
python main.py --list
```

**Output:**
```
Available test case IDs:
  ID: 1 - gmail - Find emails with subject containing 'Project report'...
  ID: 2 - gmail - Find emails mentioning 'Weekly report'...
  ID: 3 - gmail - Show emails from harisno@gdplabs.id...
  ID: 4 - gmail - Show emails sent to ticket@gdplabs.id...
  ID: 5 - gmail - Show emails from January 1, 2025 to January 31, 2025...
  ID: 6 - gmail - Show emails with label 'CATAPA Persetujuan'...
  ID: 7 - gmail - Show emails that include attachments...
  ID: 8 - gmail - Show unread emails from harisno@gdplabs.id...
  ID: 9 - gdrive - cari dan list 3 dokumen yang berjudul PRD...
  ID: 10 - gdrive - Tampilkan file yang dibuat atau berhubungan dengan harisno@gdplabs.id...
  ID: 11 - gdrive - find any documents related to "Deep Research"...
  ID: 12 - gdrive - Tampilkan dokumen yang dimodifikasi pada tanggal 1 januari 2025 - 5 januari 2025...
```

## Output Files

### Result Files

Each test case generates a result file with the naming convention:
`{id}-{codename}-{query}.txt`

**Example:** `1-gmail-Find_emails_with_subject_containing__Project_report_.txt`

**File Contents:**
```
Test Case ID: 1
Agent ID: ecca3133-e89a-49e2-8e77-03a68d13c648
Codename: gmail
Prompt: Find emails with subject containing 'Project report'
Execution Time: 2025-01-27T10:30:45.123456
Success: True
Return Code: 0
--------------------------------------------------
STDOUT:
[Agent response content here]
--------------------------------------------------
STDERR:
[Any error messages here]
--------------------------------------------------
```

### Execution Summary

`execution_summary.json` contains overall execution statistics:

```json
{
  "total": 12,
  "successful": 10,
  "failed": 2,
  "details": [
    {
      "id": "1",
      "codename": "gmail",
      "success": true
    },
    {
      "id": "2",
      "codename": "gmail",
      "success": false
    }
  ]
}
```

### Log File

`test_execution.log` contains detailed execution logs with timestamps.

## Performance Tips

1. **Parallel Workers**: Adjust the number of workers based on your system capacity and AIP SDK rate limits
2. **Batch Size**: For large test suites, consider running in smaller batches
3. **Resource Monitoring**: Monitor system resources when running many parallel workers
4. **Timeout Handling**: The script has a 5-minute timeout per test case

## Troubleshooting

### Common Issues

1. **Agent ID Not Found**
   - Verify agent IDs in your CSV file
   - Ensure agents are properly configured in AIP SDK

2. **Permission Errors**
   - Check file permissions for output directory
   - Ensure write access to the script directory

3. **Timeout Errors**
   - Some agents may take longer than 5 minutes
   - Consider increasing timeout in the script if needed

4. **CSV Format Issues**
   - Ensure proper CSV formatting with commas
   - Check for special characters in prompts that might break CSV parsing

### Debug Mode

For debugging, check the log file:
```bash
tail -f test_execution.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the log files
3. Create an issue with detailed information about your problem

---

**Happy Testing! 🚀**
