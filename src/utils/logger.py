"""
Logging module - Centralized logging configuration using loguru
"""
import sys
from pathlib import Path
from loguru import logger
from typing import Optional


class LoggerManager:
    """Manage application logging with loguru"""
    
    def __init__(
        self,
        log_dir: str = "./logs",
        log_level: str = "INFO",
        rotation: str = "10 MB",
        retention: str = "1 week",
        compression: str = "zip"
    ):
        """
        Initialize logger manager
        
        Args:
            log_dir: Directory for log files
            log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            rotation: When to rotate log files (size or time)
            retention: How long to keep old logs
            compression: Compression format for old logs
        """
        self.log_dir = Path(log_dir)
        self.log_level = log_level
        self.rotation = rotation
        self.retention = retention
        self.compression = compression
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove default handler
        logger.remove()
        
        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handlers()
        
    def _setup_console_handler(self):
        """Setup colorized console output"""
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=self.log_level,
            colorize=True
        )
        
    def _setup_file_handlers(self):
        """Setup file handlers with rotation"""
        
        # Main application log (all levels)
        logger.add(
            self.log_dir / "app.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression,
            enqueue=True  # Thread-safe
        )
        
        # Error log (ERROR and CRITICAL only)
        logger.add(
            self.log_dir / "error.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
            level="ERROR",
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )
        
        # Audit log (INFO and above, for processing audit trail)
        logger.add(
            self.log_dir / "audit.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level="INFO",
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression,
            enqueue=True,
            filter=lambda record: "audit" in record["extra"]
        )
    
    def get_logger(self):
        """Get configured logger instance"""
        return logger
    
    @staticmethod
    def audit(message: str, **kwargs):
        """
        Log an audit message
        
        Args:
            message: Audit message
            **kwargs: Additional context
        """
        logger.bind(audit=True).info(message, **kwargs)


# Global logger instance
_logger_manager: Optional[LoggerManager] = None


def init_logger(
    log_dir: str = "./logs",
    log_level: str = "INFO",
    rotation: str = "10 MB",
    retention: str = "1 week"
) -> logger:
    """
    Initialize global logger
    
    Args:
        log_dir: Directory for log files
        log_level: Minimum log level
        rotation: When to rotate log files
        retention: How long to keep old logs
        
    Returns:
        Configured logger instance
    """
    global _logger_manager
    _logger_manager = LoggerManager(
        log_dir=log_dir,
        log_level=log_level,
        rotation=rotation,
        retention=retention
    )
    return _logger_manager.get_logger()


def get_logger() -> logger:
    """
    Get global logger instance
    
    Returns:
        Logger instance
    """
    if _logger_manager is None:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")
    return _logger_manager.get_logger()


def audit_log(message: str, **kwargs):
    """
    Log an audit message
    
    Args:
        message: Audit message
        **kwargs: Additional context
    """
    if _logger_manager is None:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")
    _logger_manager.audit(message, **kwargs)
