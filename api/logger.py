import logging
import sys
import time
import functools
from typing import Any, Callable

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Setup root logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Function to get a logger for a specific module
def get_logger(name: str):
    return logging.getLogger(name)

# --- CUSTOM DECORATORS ---

def log_execution_time(func: Callable) -> Callable:
    """
    Advanced Decorator to measure and log the execution time of a function.
    Useful for monitoring performance of API endpoints and DB queries.
    """
    logger = get_logger("performance")

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        logger.info(f"Función '{func.__name__}' ejecutada en {execution_time:.4f} segundos")
        return result

    return wrapper
