.PHONY: install run run-prod list list-prod update help

install:
	pip install -r requirements.txt

# Run development tests
# Usage: make run ARGS="--ids "5,7" --workers 3"
run:
	python main.py $(ARGS)

# Run production tests
# Usage: make run-prod ARGS="--ids "5,7" --workers 3"
run-prod:
	python main.py --prod $(ARGS)

# List development test cases
list:
	python main.py --list

# List production test cases
list-prod:
	python main.py --prod --list

# Update agent list from source
update:
	python update.py

# Show help
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  run         - Run development tests (use ARGS for options)"
	@echo "  run-prod    - Run production tests (use ARGS for options)"
	@echo "  list        - List development test cases"
	@echo "  list-prod   - List production test cases"
	@echo "  update      - Update agent list from source"
	@echo "  help        - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run ARGS=\"--ids 1,3,5 --workers 3\""
	@echo "  make run-prod ARGS=\"--ids 1,3,5 --sequential\""
	@echo "  make list"
	@echo "  make list-prod"
