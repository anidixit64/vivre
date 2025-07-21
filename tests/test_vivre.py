"""
Tests for the vivre package.
"""

import pytest
from vivre import __version__, __author__, __email__


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_author():
    """Test that author is defined."""
    assert __author__ == "Aniket Dixit"


def test_email():
    """Test that email is defined."""
    assert __email__ == "anidixit64@gmail.com"


def test_import():
    """Test that the package can be imported."""
    import vivre
    assert vivre is not None 