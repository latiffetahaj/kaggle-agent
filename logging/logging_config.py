"""
Logging configuration for the LangChain Graph project.

Usage:
    import logging_config  # This sets up logging automatically
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Your message here")
"""

import logging
import sys
from pathlib import Path


LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True
):
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write logs to file
        log_to_console: Whether to print logs to console
    """
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    root_logger.handlers.clear()
    
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)
    
    if log_to_file:
        log_file = LOG_DIR / "agent.log"
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)  # More detailed in file
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
    
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logging.info("✅ Logging configured successfully")
    logging.info(f"   Level: {level}")
    logging.info(f"   Console: {log_to_console}")
    logging.info(f"   File: {log_to_file} ({log_file if log_to_file else 'N/A'})")


setup_logging()

