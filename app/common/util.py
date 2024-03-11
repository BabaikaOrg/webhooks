import logging
import multiprocessing
import os
from logging.handlers import RotatingFileHandler


def config_logger(default_log_level=logging.INFO):
    """Configure a logger that logs to both file and console.
    Log level can be passed in as a parameter, or set in the environment variable CONSOLE_LOG_LEVEL.
    If both are set, the environment variable takes precedence.
    """

    console_log_level = os.environ.get("CONSOLE_LOG_LEVEL", default_log_level)
    is_debug_env = os.environ.get("DEBUG", "false").lower() == "true"
    if is_debug_env:
        logfile_name = "latest"
    else:
        logfile_name = multiprocessing.current_process().name

    # create logs folder if not exists
    os.makedirs("logs", exist_ok=True)

    logfile_name = f"logs/{logfile_name}.log"

    file_handler = RotatingFileHandler(logfile_name, maxBytes=1000000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - line %(lineno)d - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Create a console handler that handles INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)

    third_party_packages = ["urllib3", "httpx", "uvicorn", "httpcore", "aiosqlite"]
    for package in third_party_packages:
        set_log_level(package, logging.ERROR)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler],
    )


def set_log_level(module, level):
    logger = logging.getLogger(module)
    logger.setLevel(level)
