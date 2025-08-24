import logging
import time
from functools import wraps

from rfc5424logging import Rfc5424SysLogHandler

def setup_logger():
    logger = logging.getLogger("market")
    logger.setLevel(logging.DEBUG)  # Set log level (DEBUG, INFO, WARNING, ERROR)

    # Papertrail syslog handler
    papertrail_handler = Rfc5424SysLogHandler(
        address=('logs2.papertrailapp.com', 17065),  # Use your Papertrail destination
        hostname="market",  # Optional: to identify your app
        appname="FastAPI-Logger"
    )
    papertrail_handler.setLevel(logging.DEBUG)
    papertrail_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        )
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # ✅ Capture all logs
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        )
    )

    # Attach the handler to the logger
    logger.addHandler(papertrail_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):  # Wrapper must be async
        start_time = time.perf_counter()  # Start timer
        response = await func(*args, **kwargs)  # Await the async endpoint
        end_time = time.perf_counter()  # End timer
        execution_time = end_time - start_time
        logger.info(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
        return response  # Return the response
    return wrapper
