.PHONY: install run

install:
	pip install -r requirements.txt

# Usage: make run ARGS="--ids "5,7" --workers 3"
run:
	python main.py $(ARGS)

# Usage: make update
update:
	python update.py
