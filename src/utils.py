"""
Utility functions and classes for the AIP SDK Test Script
"""

import sys
import threading
import logging

logger = logging.getLogger()


class Colors:
    """Color codes for terminal output"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels"""

    COLORS = {
        "DEBUG": Colors.CYAN,
        "INFO": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.RED + Colors.BOLD,
    }

    def format(self, record):
        # Add color to the level name
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{Colors.END}"
            )

        # Add color to the message based on level
        if record.levelno >= logging.ERROR:
            record.msg = f"{Colors.RED}{record.msg}{Colors.END}"
        elif record.levelno >= logging.WARNING:
            record.msg = f"{Colors.YELLOW}{record.msg}{Colors.END}"
        elif record.levelno >= logging.INFO:
            record.msg = f"{Colors.GREEN}{record.msg}{Colors.END}"

        return super().format(record)


def setup_logging():
    """Configure logging with colors"""
    # Get the root logger to ensure all modules can use logging
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create console handler with colored formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    # Create file handler (no colors in file)
    file_handler = logging.FileHandler("test_execution.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Thread-safe print lock
print_lock = threading.Lock()


def thread_safe_print(*args, **kwargs):
    """Thread-safe print function"""
    with print_lock:
        print(*args, **kwargs)


def parse_id_list(id_string):
    """Parse comma-separated or range-based ID list"""
    if not id_string:
        return None

    ids = set()
    for part in id_string.split(","):
        part = part.strip()
        if "-" in part and not part.startswith("-") and not part.endswith("-"):
            # Handle range (e.g., "1-5")
            try:
                start, end = map(int, part.split("-"))
                ids.update(str(i) for i in range(start, end + 1))
            except ValueError:
                logger.warning(f"Invalid range format: {part}")
        else:
            # Handle single ID
            ids.add(part)

    return list(ids)


def sanitize_filename(text):
    """Sanitize text for use in filename"""
    # Replace problematic characters with underscores
    sanitized = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in text)
    # Limit length to avoid filesystem issues
    return sanitized[:100]
