"""Module for creating and configuring loggers."""
import logging
import logging.config
import logging.handlers
import os

# Define paths for logging configuration file and log directory
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "logging.conf"
)

def get_logger(name: str, log_dir: str = None) -> logging.Logger:
    """Create and return a logger with basic configuration.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    # Load logging configuration
    logging.config.fileConfig(CONFIG_PATH, disable_existing_loggers=False)
    logger = logging.getLogger(name)
    # Add handlers if none exist
    if not logger.handlers:
        # Set logging level
        logger.setLevel(logging.INFO)
        # Define log format
        formatter = logging.Formatter(
            fmt=(
                "[%(asctime)s][%(name)s][%(module)s][%(funcName)s][%(levelname)s]:"
                " %(message)s"
            )
        )
        if log_dir:
            # Configure file handler
            log_path = os.path.join(log_dir, name)
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=f"{log_path}.log", when="D", interval=1, backupCount=180
            )
            file_handler.setFormatter(formatter)
            file_handler.suffix = "%Y%m%d.log"
            logger.addHandler(file_handler)

        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)

    # Disable log propagation
    logger.propagate = False
    return logger

def create_log_folder(base_log_path: str, sub_folder: str = "default") -> str:
    """Create log directory if it doesn't exist.

    Args:
        base_log_path (str): The base directory where logs should be stored.
        sub_folder (str, optional): An optional sub-folder name. Defaults to "default".

    Returns:
        str: Path to the log directory
    """
    log_path = os.path.join(base_log_path, sub_folder)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        get_logger(__name__).info("Log directory created: %s", log_path)
    return log_path