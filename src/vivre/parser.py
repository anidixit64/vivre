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

        This method performs comprehensive validation including:
        - Input path validation (None, empty, invalid characters)
        - File existence and accessibility checks
        - EPUB format validation (ZIP structure, required files)
        - Corrupted file detection

        Args:
            file_path: Path to the EPUB file to load (str or Path object)

        Returns:
            True if the file was successfully loaded, False otherwise

        Raises:
            FileNotFoundError: If the EPUB file doesn't exist
            ValueError: If the file path is invalid, file is not readable,
                       or file is not a valid EPUB (empty, corrupted, wrong format)
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
                # Check if file is empty
                f.seek(0, 2)  # Seek to end
                file_size = f.tell()
                if file_size == 0:
                    raise ValueError(
                        f"File is not a valid EPUB (empty file): {file_path}"
                    )

                # Check if file is too small to be a valid ZIP
                if file_size < 4:
                    raise ValueError(
                        f"File is not a valid EPUB (file too small): {file_path}"
                    )

                # Check ZIP magic number
                f.seek(0)  # Seek to beginning
                magic = f.read(4)
                if magic != b"PK\x03\x04":
                    raise ValueError(
                        f"File is not a valid EPUB (not a ZIP archive): {file_path}"
                    )

                # Try to open as ZIP to validate structure
                try:
                    with zipfile.ZipFile(file_path, "r") as test_zip:
                        # Check if it has the minimum required files for an EPUB
                        file_list = test_zip.namelist()
                        if "META-INF/container.xml" not in file_list:
                            raise ValueError(
                                f"File is not a valid EPUB "
                                f"(missing container.xml): {file_path}"
                            )
                except zipfile.BadZipFile:
                    raise ValueError(
                        f"File is not a valid EPUB "
                        f"(corrupted ZIP structure): {file_path}"
                    )
        except Exception as e:
            if "File is not a valid EPUB" in str(e):
                raise  # Re-raise our specific validation errors
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

        This method performs the same comprehensive validation as load_epub
        and then extracts chapter content from the EPUB file.

        Args:
            file_path: Path to the EPUB file to parse (str or Path object)

        Returns:
            List of tuples containing (chapter_title, chapter_text) pairs

        Raises:
            FileNotFoundError: If the EPUB file doesn't exist
            ValueError: If the file path is invalid, file is not a valid EPUB,
                       or the EPUB structure cannot be parsed
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

                # Step 3: Extract chapter titles from table of contents
                chapter_titles = self._extract_chapter_titles(epub_zip, content_dir)

                # Find the spine to get the reading order
                spine_elem = content_root.find(".//{*}spine")
                if spine_elem is None:
                    raise ValueError("Could not find spine in content.opf")

                # Get all itemref elements in the spine
                itemrefs = spine_elem.findall(".//{*}itemref")
                if not itemrefs:
                    raise ValueError("No itemref elements found in spine")

                # Step 4: Extract chapter content for each item in the spine
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

                    # Skip non-story content based on href pattern
                    if self._is_title_or_cover_page("", href):
                        continue

                    # Construct the full path to the chapter file
                    chapter_path = content_dir / href

                    # Read and parse the chapter file
                    try:
                        chapter_content = epub_zip.read(str(chapter_path))
                        chapter_title, chapter_text = self._extract_chapter_content(
                            chapter_content
                        )

                        # Use title from table of contents if available
                        if href in chapter_titles:
                            chapter_title = chapter_titles[href]

                        # Skip if still a generic title
                        if self._is_generic_title(chapter_title):
                            continue

                        # Skip if text is too short (likely just a title page)
                        if len(chapter_text.strip()) < 100:
                            continue

                        # Skip back matter (files with 'bm' in the name)
                        if "bm" in href.lower():
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
                title_text = title_elem.text.strip()
                # Skip generic titles that are likely not chapter titles
                if title_text and not self._is_generic_title(title_text):
                    return title_text

        # If no title found, try to get the first h1 or h2 text
        for tag in ["h1", "h2", "h3"]:
            for elem in root.iter():
                if elem.tag.endswith(tag) and elem.text and elem.text.strip():
                    title_text = elem.text.strip()
                    if not self._is_generic_title(title_text):
                        return title_text

        return "Untitled Chapter"

    def _is_generic_title(self, title: str) -> bool:
        """
        Check if a title is generic and likely not a chapter title.

        Args:
            title: The title to check

        Returns:
            True if the title is generic, False otherwise
        """
        title_lower = title.lower()

        # Generic titles that are likely not chapter titles
        generic_titles = [
            "magic tree house",
            "vacation under the volcano",
            "vacaciones al pie de un volcán",
            "percy jackson",
            "the lightning thief",
            "el ladrón del rayo",
        ]

        # Check if title matches any generic title
        for generic in generic_titles:
            if generic in title_lower:
                return True

        # Check if title is too short (likely not a chapter title)
        if len(title.strip()) < 3:
            return True

        # Check if title is just the book title repeated
        if title_lower.count(title_lower.split()[0]) > 1:
            return True

        return False

    def _extract_chapter_titles(
        self, epub_zip: zipfile.ZipFile, content_dir: Path
    ) -> dict:
        """
        Extract chapter titles from the table of contents.

        Args:
            epub_zip: The EPUB zip file
            content_dir: Base directory for content files

        Returns:
            Dictionary mapping href to chapter title
        """
        chapter_titles = {}

        try:
            # Look for table of contents file
            toc_files = ["toc.ncx", "OEBPS/toc.ncx", "OEBPS/html/toc.ncx"]

            toc_content = None
            for toc_file in toc_files:
                try:
                    toc_content = epub_zip.read(toc_file)
                    break
                except KeyError:
                    continue

            if toc_content:
                # Parse NCX file for chapter titles
                toc_root = ET.fromstring(toc_content)
                nav_points = toc_root.findall(".//{*}navPoint")

                for nav_point in nav_points:
                    # Get the title
                    title_elem = nav_point.find(".//{*}text")
                    if title_elem is not None and title_elem.text:
                        title = title_elem.text.strip()

                        # Get the href
                        content_elem = nav_point.find(".//{*}content")
                        if content_elem is not None:
                            src = content_elem.get("src")
                            if src:
                                # Extract the filename from src (remove anchor)
                                href = src.split("#")[0]
                                chapter_titles[href] = title

        except Exception as e:
            print(f"Warning: Could not extract chapter titles from TOC: {e}")

        # If NCX parsing failed, try to find HTML TOC
        if not chapter_titles:
            try:
                # Look for HTML table of contents
                toc_html_files = [
                    "OEBPS/Osbo_9780375894701_epub_toc_r1.htm",
                    "OEBPS/html/toc.html",
                    "toc.html",
                ]

                for toc_file in toc_html_files:
                    try:
                        toc_content = epub_zip.read(toc_file)
                        break
                    except KeyError:
                        continue
                else:
                    return chapter_titles

                # Parse HTML TOC for chapter links
                toc_root = ET.fromstring(toc_content)
                links = toc_root.findall(".//{*}a")

                for link in links:
                    href = link.get("href")
                    if href and link.text:
                        title = link.text.strip()
                        # Clean up href (remove anchor if present)
                        href = href.split("#")[0]
                        chapter_titles[href] = title

            except Exception as e:
                print(f"Warning: Could not extract chapter titles from HTML TOC: {e}")

        return chapter_titles

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
            title_text = title_match.group(1).strip()
            if not self._is_generic_title(title_text):
                return title_text

        # Look for h1 tags
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            title_text = h1_match.group(1).strip()
            if not self._is_generic_title(title_text):
                return title_text

        # Look for h2 tags
        h2_match = re.search(r"<h2[^>]*>(.*?)</h2>", content, re.IGNORECASE | re.DOTALL)
        if h2_match:
            title_text = h2_match.group(1).strip()
            if not self._is_generic_title(title_text):
                return title_text

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
        Check if a chapter is a title, cover page, or other non-story content.

        Args:
            title: The chapter title
            href: The chapter file path

        Returns:
            True if the chapter should be ignored, False otherwise
        """
        # Check title for common non-story content indicators
        title_lower = title.lower()
        non_story_keywords = [
            "cover",
            "title",
            "titlepage",
            "front cover",
            "back cover",
            "acknowledgement",
            "acknowledgments",
            "acknowledgements",
            "table of contents",
            "contents",
            "toc",
            "copyright",
            "legal",
            "disclaimer",
            "about the author",
            "author bio",
            "biography",
            "translator",
            "translation",
            "translator's note",
            "preface",
            "foreword",
            "introduction",
            "prologue",
            "epilogue",
            "afterword",
            "appendix",
            "index",
            "bibliography",
            "references",
            "citations",
            "notes",
            "glossary",
            "credits",
            "dedication",
            "colophon",
        ]

        if any(keyword in title_lower for keyword in non_story_keywords):
            return True

        # Check href for common non-story file patterns
        href_lower = href.lower()
        non_story_patterns = [
            "cover",
            "title",
            "titlepage",
            "front",
            "back",
            "toc",
            "contents",
            "copyright",
            "legal",
            "acknowledgement",
            "preface",
            "foreword",
            "epilogue",
            "afterword",
            "appendix",
            "index",
            "bibliography",
            "references",
            "glossary",
            "fm",
            "ded",
            "cop",
            "adc",
            "author",
        ]

        if any(pattern in href_lower for pattern in non_story_patterns):
            return True

        # Check for specific file patterns that indicate non-story content
        # Front matter files (fm1, fm2, etc.)
        if re.search(r"fm\d+", href_lower):
            return True

        # Dedication files
        if re.search(r"ded", href_lower):
            return True

        # Copyright files
        if re.search(r"cop", href_lower):
            return True

        # Acknowledgements files
        if re.search(r"adc", href_lower):
            return True

        # Front split files
        if re.search(r"front_split", href_lower):
            return True

        return False
