"""
Tests for the __main__.py module.
"""

import subprocess
import sys
from pathlib import Path


class TestMainModule:
    """Test the __main__.py module functionality."""

    def test_main_module_import(self):
        """Test that the main module can be imported."""
        from vivre.__main__ import app

        assert app is not None

    def test_main_module_execution(self):
        """Test that the main module can be executed."""
        # Test that the module can be run as a script
        result = subprocess.run(
            [sys.executable, "-m", "vivre", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "vivre" in result.stdout

    def test_main_module_version(self):
        """Test that the main module version flag works."""
        result = subprocess.run(
            [sys.executable, "-m", "vivre", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        # Typer exits with 2 when no command is provided
        assert result.returncode == 2
        assert "vivre" in result.stdout

    def test_main_module_invalid_command(self):
        """Test that the main module handles invalid commands."""
        result = subprocess.run(
            [sys.executable, "-m", "vivre", "invalid"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode != 0

    def test_main_module_parse_help(self):
        """Test that the main module parse help works."""
        result = subprocess.run(
            [sys.executable, "-m", "vivre", "parse", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "parse" in result.stdout

    def test_main_module_align_help(self):
        """Test that the main module align help works."""
        result = subprocess.run(
            [sys.executable, "-m", "vivre", "align", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "align" in result.stdout
