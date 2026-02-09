"""
AI Resume Screener - Logging Configuration
Configures logging for the application.
"""
import logging
import logging.handlers
from pathlib import Path

# Log directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log files
APPLICATION_LOG = LOG_DIR / "application.log"
ERROR_LOG = LOG_DIR / "errors.log"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log levels
DEFAULT_LOG_LEVEL = logging.INFO
ERROR_LOG_LEVEL = logging.ERROR


def setup_logging(name: str = "ai_resume_screener") -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(console_handler)
    
    # Application file handler (rotating)
    app_handler = logging.handlers.RotatingFileHandler(
        APPLICATION_LOG,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    app_handler.setLevel(DEFAULT_LOG_LEVEL)
    app_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(app_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    error_handler.setLevel(ERROR_LOG_LEVEL)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(error_handler)
    
    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        module_name: Name of the module requesting the logger
        
    Returns:
        Logger instance for the module
    """
    return logging.getLogger(f"ai_resume_screener.{module_name}")


# Initialize default logger
logger = setup_logging()
