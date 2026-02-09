"""
File Handler Module
Utilities for file I/O operations.
"""
import json
from pathlib import Path
from typing import Any, Optional, Union

from config.logging_config import get_logger

logger = get_logger("file_handler")


def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """Read text file contents."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding=encoding)


def write_file(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
    """Write content to text file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    logger.info(f"Written file: {file_path}")


def read_json(file_path: Union[str, Path]) -> Any:
    """Read JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> None:
    """Write data to JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    logger.info(f"Written JSON: {file_path}")


def ensure_dir(dir_path: Union[str, Path]) -> Path:
    """Ensure directory exists."""
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(dir_path: Union[str, Path], pattern: str = "*") -> list:
    """List files matching pattern in directory."""
    path = Path(dir_path)
    return list(path.glob(pattern))
