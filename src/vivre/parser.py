"""
EPUB Parser module for the vivre library.

This module provides functionality to load and validate EPUB files.
"""

import os
import re
import zipfile
from pathlib import Path
from typing import Any, List, Optional, Tuple

from defusedxml import ElementTree as ET


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
        # Validate input path
        if file_path is None:
            raise ValueError("File path cannot be None")

        # Convert to string for validation
        if isinstance(file_path, (str, Path)):
            path_str = str(file_path).strip()
        else:
            raise ValueError(
                f"File path must be a string or Path object, "
                f"not {type(file_path).__name__}"
            )

        # Check for empty or whitespace-only paths
        if not path_str:
            raise ValueError("File path cannot be empty")

        # Check for invalid characters in path
        invalid_chars = ["\x00", "\n", "\r", "\t"]
        for char in invalid_chars:
            if char in path_str:
                raise ValueError("File path contains invalid characters")

        # Convert to Path object
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

    def parse_epub(self, file_path: Path) -> List[Tuple[str, str]]:
        """
        Parse an EPUB file and extract chapter titles and text content.

        Args:
            file_path: Path to the EPUB file to parse

        Returns:
            List of tuples containing (chapter_title, chapter_text) pairs

        Raises:
            FileNotFoundError: If the EPUB file doesn't exist
            ValueError: If the file is not a valid EPUB or cannot be parsed
        """
        # Validate input path (same validation as load_epub)
        if file_path is None:
            raise ValueError("File path cannot be None")

        # Convert to string for validation
        if isinstance(file_path, (str, Path)):
            path_str = str(file_path).strip()
        else:
            raise ValueError(
                f"File path must be a string or Path object, "
                f"not {type(file_path).__name__}"
            )

        # Check for empty or whitespace-only paths
        if not path_str:
            raise ValueError("File path cannot be empty")

        # Check for invalid characters in path
        invalid_chars = ["\x00", "\n", "\r", "\t"]
        for char in invalid_chars:
            if char in path_str:
                raise ValueError("File path contains invalid characters")

        # Validate the file first
        if not self.load_epub(file_path):
            raise ValueError(f"Failed to load EPUB file: {file_path}")

        chapters = []

        try:
            with zipfile.ZipFile(file_path, "r") as epub_zip:
                # Step 1: Find the container.xml to locate the content.opf
                container_xml = epub_zip.read("META-INF/container.xml")
                container_root = ET.fromstring(container_xml)

                # Extract the path to the content.opf file
                # Look for the rootfile element with
                # media-type="application/oebps-package+xml"
                rootfile_elem = container_root.find(
                    './/{*}rootfile[@media-type="application/oebps-package+xml"]'
                )
                if rootfile_elem is None:
                    raise ValueError("Could not find content.opf in container.xml")

                content_opf_path = rootfile_elem.get("full-path")
                if not content_opf_path:
                    raise ValueError("No full-path attribute found in rootfile")

                # Step 2: Parse the content.opf to get the spine (reading order)
                content_opf = epub_zip.read(content_opf_path)
                content_root = ET.fromstring(content_opf)

                # Get the base directory for the content files
                content_dir = Path(content_opf_path).parent

                # Find the spine to get the reading order
                spine_elem = content_root.find(".//{*}spine")
                if spine_elem is None:
                    raise ValueError("Could not find spine in content.opf")

                # Get all itemref elements in the spine
                itemrefs = spine_elem.findall(".//{*}itemref")
                if not itemrefs:
                    raise ValueError("No itemref elements found in spine")

                # Step 3: Extract chapter content for each item in the spine
                for itemref in itemrefs:
                    idref = itemref.get("idref")
                    if not idref:
                        continue

                    # Find the manifest item with this id
                    manifest_elem = content_root.find(".//{*}manifest")
                    if manifest_elem is None:
                        continue

                    item_elem = manifest_elem.find(f'.//{{*}}item[@id="{idref}"]')
                    if item_elem is None:
                        continue

                    href = item_elem.get("href")
                    if not href:
                        continue

                    # Construct the full path to the chapter file
                    chapter_path = content_dir / href

                    # Read and parse the chapter file
                    try:
                        chapter_content = epub_zip.read(str(chapter_path))
                        chapter_title, chapter_text = self._extract_chapter_content(
                            chapter_content
                        )

                        # Skip title/cover pages
                        if self._is_title_or_cover_page(chapter_title, href):
                            continue

                        chapters.append((chapter_title, chapter_text))
                    except Exception as e:
                        # Skip chapters that can't be parsed
                        print(f"Warning: Could not parse chapter {href}: {e}")
                        continue

        except zipfile.BadZipFile:
            raise ValueError(f"File is not a valid ZIP archive: {file_path}")
        except ET.ParseError as e:
            raise ValueError(f"Error parsing EPUB XML: {e}")
        except Exception as e:
            raise ValueError(f"Error reading EPUB file: {e}")

        return chapters

    def _extract_chapter_content(self, chapter_content: bytes) -> Tuple[str, str]:
        """
        Extract chapter title and text from HTML/XML content.

        Args:
            chapter_content: Raw bytes of the chapter file

        Returns:
            Tuple of (chapter_title, chapter_text)
        """
        try:
            # Parse the HTML/XML content
            root = ET.fromstring(chapter_content)

            # Try to find the title in various ways
            title = self._extract_title(root)

            # Extract all text content
            text = self._extract_text(root)

            return title, text

        except ET.ParseError:
            # If XML parsing fails, try to extract text using regex
            content_str = chapter_content.decode("utf-8", errors="ignore")
            title = self._extract_title_fallback(content_str)
            text = self._extract_text_fallback(content_str)
            return title, text

    def _extract_title(self, root: Any) -> str:
        """Extract title from XML element."""
        # Try different possible title locations
        title_selectors = [
            ".//{*}title",
            ".//{*}h1",
            ".//{*}h2",
            ".//{*}h3",
            ".//{*}head/{*}title",
        ]

        for selector in title_selectors:
            title_elem = root.find(selector)
            if title_elem is not None and title_elem.text:
                return title_elem.text.strip()

        # If no title found, try to get the first h1 or h2 text
        for tag in ["h1", "h2", "h3"]:
            for elem in root.iter():
                if elem.tag.endswith(tag) and elem.text and elem.text.strip():
                    return elem.text.strip()

        return "Untitled Chapter"

    def _extract_text(self, root: Any) -> str:
        """Extract all text content from XML element."""
        # Get all text from body or root
        body = root.find(".//{*}body")
        if body is not None:
            root = body

        # Extract all text content
        text_parts = []
        for elem in root.iter():
            if elem.text and elem.text.strip():
                text_parts.append(elem.text.strip())
            if elem.tail and elem.tail.strip():
                text_parts.append(elem.tail.strip())

        text = " ".join(text_parts)

        # Clean up the text
        text = re.sub(
            r"\s+", " ", text
        )  # Replace multiple whitespace with single space
        text = text.strip()

        return text

    def _extract_title_fallback(self, content: str) -> str:
        """Fallback title extraction using regex."""
        # Look for title tags
        title_match = re.search(
            r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL
        )
        if title_match:
            return title_match.group(1).strip()

        # Look for h1 tags
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            return h1_match.group(1).strip()

        return "Untitled Chapter"

    def _extract_text_fallback(self, content: str) -> str:
        """Fallback text extraction using regex."""
        # Remove HTML tags and extract text
        # First remove script and style tags
        content = re.sub(
            r"<script[^>]*>.*?</script>", "", content, flags=re.IGNORECASE | re.DOTALL
        )
        content = re.sub(
            r"<style[^>]*>.*?</style>", "", content, flags=re.IGNORECASE | re.DOTALL
        )

        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)

        # Clean up whitespace
        content = re.sub(r"\s+", " ", content)

        return content.strip()

    def _is_title_or_cover_page(self, title: str, href: str) -> bool:
        """
        Check if a chapter is a title or cover page that should be ignored.

        Args:
            title: The chapter title
            href: The chapter file path

        Returns:
            True if the chapter should be ignored, False otherwise
        """
        # Check title for common cover/title indicators
        title_lower = title.lower()
        if any(
            keyword in title_lower
            for keyword in ["cover", "title", "titlepage", "front cover", "back cover"]
        ):
            return True

        # Check href for common cover/title file patterns
        href_lower = href.lower()
        if any(
            pattern in href_lower
            for pattern in ["cover", "title", "titlepage", "front", "back"]
        ):
            return True

        return False
