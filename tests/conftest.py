# tests/conftest.py
from pathlib import Path

import pytest

from vivre.api import Chapters
from vivre.integration import VivrePipeline
from vivre.parser import VivreParser
from vivre.segmenter import Segmenter


@pytest.fixture(scope="session")
def segmenter() -> Segmenter:
    """
    A session-scoped fixture that provides a single, shared Segmenter instance.
    This prevents spaCy models from being reloaded for every test.
    """
    print("\n--- Initializing Segmenter (once per session) ---")
    return Segmenter()


@pytest.fixture(scope="session")
def source_epub_path() -> Path:
    return (
        Path(__file__).parent
        / "data"
        / "Vacation Under the Volcano - Mary Pope Osborne.epub"
    )


@pytest.fixture(scope="session")
def target_epub_path() -> Path:
    return Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"


@pytest.fixture(scope="session")
def source_chapters(source_epub_path: Path) -> Chapters:
    """
    A session-scoped fixture that parses the source EPUB file once.
    """
    print(f"\n--- Parsing {source_epub_path.name} (once per session) ---")
    parser = VivreParser()
    chapters_list = parser.parse_epub(source_epub_path)
    return Chapters(chapters_list, book_title="")


@pytest.fixture(scope="session")
def target_chapters(target_epub_path: Path) -> Chapters:
    """
    A session-scoped fixture that parses the target EPUB file once.
    """
    print(f"\n--- Parsing {target_epub_path.name} (once per session) ---")
    parser = VivreParser()
    chapters_list = parser.parse_epub(target_epub_path)
    return Chapters(chapters_list, book_title="")


@pytest.fixture(scope="session")
def default_pipeline() -> VivrePipeline:
    """A session-scoped fixture for the default en-es pipeline."""
    print("\n--- Initializing VivrePipeline (once per session) ---")
    return VivrePipeline("en-es")


@pytest.fixture(scope="session")
def epub_path() -> Path:
    """A session-scoped fixture for a single EPUB file (for CLI tests)."""
    return (
        Path(__file__).parent
        / "data"
        / "Vacation Under the Volcano - Mary Pope Osborne.epub"
    )
