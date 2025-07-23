"""
EPUB Parser module for the vivre library.

This module provides functionality to load and validate EPUB files.
"""

import os
from pathlib import Path
from typing import Optional


class Parser:
    """
    A parser for EPUB files.

    This class provides methods to load and validate EPUB files.
    """

    def __init__(self) -> None:
        """Initialize the Parser."""
        self.file_path: Optional[Path] = None
        self._is_loaded: bool = False

    def load_epub(self, file_path: Path) -> bool:
        """
        Load an EPUB file from the given path.

        Args:
            file_path: Path to the EPUB file to load

        Returns:
            True if the file was successfully loaded, False otherwise

        Raises:
            FileNotFoundError: If the EPUB file doesn't exist
            ValueError: If the file is not readable or not a valid EPUB
        """
        file_path = Path(file_path)

        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"EPUB file not found: {file_path}")

        # Check if it's a file
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            raise ValueError(f"EPUB file is not readable: {file_path}")

        # Basic EPUB validation - check if it's a ZIP file (EPUBs are ZIP archives)
        try:
            with open(file_path, "rb") as f:
                # Check ZIP magic number
                magic = f.read(4)
                if magic != b"PK\x03\x04":
                    raise ValueError(
                        f"File is not a valid EPUB (not a ZIP archive): {file_path}"
                    )
        except Exception as e:
            raise ValueError(f"Error reading EPUB file: {e}")

            # If we get here, the file is valid
        self.file_path = file_path
        self._is_loaded = True
        return True

    def is_loaded(self) -> bool:
        """Check if an EPUB file is currently loaded."""
        return self._is_loaded
