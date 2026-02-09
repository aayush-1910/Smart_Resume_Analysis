"""
Logger Module
Re-exports logging configuration for convenience.
"""
from config.logging_config import get_logger, setup_logging

__all__ = ['get_logger', 'setup_logging']
