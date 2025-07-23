"""
Tests for parser functionality.
"""

from pathlib import Path

import pytest


class TestParser:
    """Test cases for parser functionality."""

    def test_parser_initialization(self):
        """Test that Parser can be initialized."""
        from vivre.parser import Parser

        parser = Parser()
        assert parser is not None
        assert not parser.is_loaded

    def test_load_english_epub(self):
        """Test loading the English EPUB file."""
        from vivre.parser import Parser

        # Get path to English test EPUB file
        test_file_path = (
            Path(__file__).parent
            / "data"
            / "Percy Jackson 1 - The Lightning Thief - Riordan, Rick.epub"
        )

        # Verify test file exists
        assert test_file_path.exists(), f"Test file not found: {test_file_path}"
        assert test_file_path.is_file(), f"Path is not a file: {test_file_path}"

        # Initialize parser and load EPUB
        parser = Parser()
        result = parser.load_epub(test_file_path)

        # Check if file was loaded successfully
        assert result is True, "EPUB should be loaded successfully"
        assert parser.is_loaded, "Parser should indicate file is loaded"
        assert (
            parser.file_path == test_file_path
        ), "Parser should store the correct file path"

    def test_load_spanish_epub(self):
        """Test loading the Spanish EPUB file."""
        from vivre.parser import Parser

        # Get path to Spanish test EPUB file
        test_file_path = (
            Path(__file__).parent / "data" / "El ladrón del rayo - Rick Riordan.epub"
        )

        # Verify test file exists
        assert test_file_path.exists(), f"Test file not found: {test_file_path}"
        assert test_file_path.is_file(), f"Path is not a file: {test_file_path}"

        # Initialize parser and load EPUB
        parser = Parser()
        result = parser.load_epub(test_file_path)

        # Check if file was loaded successfully
        assert result is True, "EPUB should be loaded successfully"
        assert parser.is_loaded, "Parser should indicate file is loaded"
        assert (
            parser.file_path == test_file_path
        ), "Parser should store the correct file path"

    def test_load_nonexistent_file(self):
        """Test that loading a nonexistent file raises FileNotFoundError."""
        from vivre.parser import Parser

        parser = Parser()
        nonexistent_path = Path(__file__).parent / "data" / "nonexistent.epub"

        with pytest.raises(FileNotFoundError):
            parser.load_epub(nonexistent_path)

    def test_load_directory_instead_of_file(self):
        """Test that loading a directory raises ValueError."""
        from vivre.parser import Parser

        parser = Parser()
        directory_path = Path(__file__).parent / "data"

        with pytest.raises(ValueError, match="Path is not a file"):
            parser.load_epub(directory_path)
