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
        assert not parser.is_loaded()

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
        assert parser.is_loaded(), "Parser should indicate file is loaded"
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
        assert parser.is_loaded(), "Parser should indicate file is loaded"
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

    def test_load_invalid_epub_file(self):
        """Test that loading a non-ZIP file raises ValueError."""
        import tempfile

        from vivre.parser import Parser

        parser = Parser()

        # Create a temporary file that's not a ZIP
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            temp_file.write(b"This is not a ZIP file")
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            # Clean up
            temp_file_path.unlink()

    def test_load_unreadable_file(self):
        """Test that loading an unreadable file raises ValueError."""
        import os
        import tempfile

        from vivre.parser import Parser

        parser = Parser()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            temp_file.write(b"PK\x03\x04fake zip content")
            temp_file_path = Path(temp_file.name)

        try:
            # Make file unreadable
            os.chmod(temp_file_path, 0o000)

            with pytest.raises(ValueError, match="not readable"):
                parser.load_epub(temp_file_path)
        finally:
            # Clean up - make readable first
            os.chmod(temp_file_path, 0o644)
            temp_file_path.unlink()

    def test_parse_english_epub(self):
        """Test parsing the English EPUB file to extract chapters."""
        from vivre.parser import Parser

        # Get path to English test EPUB file
        test_file_path = (
            Path(__file__).parent
            / "data"
            / "Percy Jackson 1 - The Lightning Thief - Riordan, Rick.epub"
        )

        # Verify test file exists
        assert test_file_path.exists(), f"Test file not found: {test_file_path}"

        # Initialize parser and parse EPUB
        parser = Parser()
        chapters = parser.parse_epub(test_file_path)

        # Verify the structure and content
        assert isinstance(chapters, list), "chapters should be a list"
        assert len(chapters) > 0, "should extract at least one chapter"

        for i, (title, text) in enumerate(chapters):
            assert isinstance(title, str), f"chapter {i} title should be a string"
            assert isinstance(text, str), f"chapter {i} text should be a string"
            assert len(title) > 0, f"chapter {i} title should not be empty"
            # Skip text length check for cover/title pages
            if "cover" not in title.lower() and "title" not in title.lower():
                assert len(text) > 0, f"chapter {i} text should not be empty"
            print(f"Chapter {i+1}: {title[:50]}...")
            print(f"Text length: {len(text)} characters")

    def test_extract_chapter_content_fallback(self):
        """Test the fallback text extraction when XML parsing fails."""
        from vivre.parser import Parser

        parser = Parser()

        # Test with malformed HTML that will cause XML parsing to fail
        malformed_html = (
            b"<html><body><h1>Test Chapter</h1><p>This is some text</p><unclosed_tag>"
        )

        title, text = parser._extract_chapter_content(malformed_html)

        assert isinstance(title, str)
        assert isinstance(text, str)
        assert len(title) > 0
        assert len(text) > 0
        assert "Test Chapter" in title or "Test Chapter" in text

    def test_parse_epub_missing_rootfile(self):
        """Test parsing EPUB with missing rootfile element."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with container.xml but missing rootfile
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml without rootfile
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

        try:
            with pytest.raises(
                ValueError, match="Could not find content.opf in container.xml"
            ):
                parser.parse_epub(Path(tmp_file.name))
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_missing_full_path(self):
        """Test parsing EPUB with missing full-path attribute."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with rootfile but missing full-path
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml with rootfile but no full-path
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

        try:
            with pytest.raises(
                ValueError, match="No full-path attribute found in rootfile"
            ):
                parser.parse_epub(Path(tmp_file.name))
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_empty_spine(self):
        """Test parsing EPUB with empty spine."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with empty spine
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

                # Add content.opf with empty spine
                content_opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata>
    <dc:title>Test Book</dc:title>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
  </spine>
</package>"""
                zip_file.writestr("content.opf", content_opf)

        try:
            with pytest.raises(ValueError, match="Error parsing EPUB XML"):
                parser.parse_epub(Path(tmp_file.name))
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_missing_spine_with_valid_xml(self):
        """Test parsing EPUB with missing spine but valid XML."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with valid XML but missing spine
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

                # Add content.opf without spine
                content_opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata>
    <dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">Test Book</dc:title>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
</package>"""
                zip_file.writestr("content.opf", content_opf)

        try:
            with pytest.raises(ValueError, match="Could not find spine in content.opf"):
                parser.parse_epub(Path(tmp_file.name))
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_empty_itemrefs(self):
        """Test parsing EPUB with empty itemrefs in spine."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with empty itemrefs in spine
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

                # Add content.opf with empty itemrefs in spine
                content_opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata>
    <dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">Test Book</dc:title>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref=""/>
  </spine>
</package>"""
                zip_file.writestr("content.opf", content_opf)

        try:
            # Empty idrefs are skipped, so this should return an empty list
            chapters = parser.parse_epub(Path(tmp_file.name))
            assert (
                chapters == []
            ), "Should return empty list when all itemrefs have empty idrefs"
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_missing_manifest(self):
        """Test parsing EPUB with missing manifest."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with missing manifest
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

                # Add content.opf without manifest
                content_opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata>
    <dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">Test Book</dc:title>
  </metadata>
  <spine>
    <itemref idref="chapter1"/>
  </spine>
</package>"""
                zip_file.writestr("content.opf", content_opf)

        try:
            # Missing manifest should result in empty chapters list
            chapters = parser.parse_epub(Path(tmp_file.name))
            assert chapters == [], "Should return empty list when manifest is missing"
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_malformed_structure(self):
        """Test parsing EPUB with malformed structure."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create a malformed EPUB (ZIP file without proper EPUB structure)
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add a file that's not container.xml
                zip_file.writestr("test.txt", "This is not an EPUB")

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.parse_epub(Path(tmp_file.name))
        finally:
            os.unlink(tmp_file.name)

    def test_parse_epub_missing_spine(self):
        """Test parsing EPUB with missing spine."""
        import os
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Create an EPUB with container.xml but missing spine
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, "w") as zip_file:
                # Add container.xml
                container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
                zip_file.writestr("META-INF/container.xml", container_xml)

                # Add content.opf without spine
                content_opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata>
    <dc:title>Test Book</dc:title>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
</package>"""
                zip_file.writestr("content.opf", content_opf)

        try:
            with pytest.raises(ValueError, match="Error parsing EPUB XML"):
                parser.parse_epub(Path(tmp_file.name))
        finally:
            os.unlink(tmp_file.name)

    def test_is_title_or_cover_page_method(self):
        """Test the _is_non_story_content method."""
        from vivre.parser import Parser

        parser = Parser()

        # Test title-based filtering
        assert parser._is_non_story_content("Cover", "chapter1.xhtml") is True
        assert parser._is_non_story_content("Title Page", "chapter1.xhtml") is True
        assert parser._is_non_story_content("Front Cover", "chapter1.xhtml") is True
        assert parser._is_non_story_content("Back Cover", "chapter1.xhtml") is True
        assert parser._is_non_story_content("TitlePage", "chapter1.xhtml") is True

        # Test href-based filtering
        assert parser._is_non_story_content("Chapter 1", "cover.xhtml") is True
        assert parser._is_non_story_content("Chapter 1", "titlepage.xhtml") is True
        assert parser._is_non_story_content("Chapter 1", "front.xhtml") is True
        assert parser._is_non_story_content("Chapter 1", "back.xhtml") is True

        # Test normal chapters (should not be filtered)
        assert parser._is_non_story_content("Chapter 1", "chapter1.xhtml") is False
        assert parser._is_non_story_content("The Beginning", "part1.xhtml") is False
        assert parser._is_non_story_content("Percy Jackson", "part2.xhtml") is False

    def test_parse_spanish_epub(self):
        """Test parsing the Spanish EPUB file to extract chapters."""
        from vivre.parser import Parser

        # Get path to Spanish test EPUB file
        test_file_path = (
            Path(__file__).parent / "data" / "El ladrón del rayo - Rick Riordan.epub"
        )

        # Verify test file exists
        assert test_file_path.exists(), f"Test file not found: {test_file_path}"

        # Initialize parser and parse EPUB
        parser = Parser()
        chapters = parser.parse_epub(test_file_path)

        # Verify the structure and content
        assert isinstance(chapters, list), "chapters should be a list"
        assert len(chapters) > 0, "should extract at least one chapter"

        for i, (title, text) in enumerate(chapters):
            assert isinstance(title, str), f"chapter {i} title should be a string"
            assert isinstance(text, str), f"chapter {i} text should be a string"
            assert len(title) > 0, f"chapter {i} title should not be empty"
            # Skip text length check for cover/title pages
            if "cover" not in title.lower() and "title" not in title.lower():
                assert len(text) > 0, f"chapter {i} text should not be empty"
            print(f"Chapter {i+1}: {title[:50]}...")
            print(f"Text length: {len(text)} characters")

    def test_parse_epub_error_handling(self):
        """Test error handling in parse_epub method."""
        from vivre.parser import Parser

        parser = Parser()

        # Test with non-existent file
        with pytest.raises(FileNotFoundError, match="EPUB file not found"):
            parser.parse_epub(Path("nonexistent.epub"))

        # Test with invalid EPUB (not a ZIP file)
        invalid_epub = Path(__file__).parent / "data" / "invalid.epub"
        invalid_epub.write_text("This is not an EPUB file")

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.parse_epub(invalid_epub)
        finally:
            invalid_epub.unlink()  # Clean up

    def test_parse_epub_structure(self):
        """Test that parse_epub returns the correct data structure."""
        from vivre.parser import Parser

        # Get path to English test EPUB file
        test_file_path = (
            Path(__file__).parent
            / "data"
            / "Percy Jackson 1 - The Lightning Thief - Riordan, Rick.epub"
        )

        # Verify test file exists
        assert test_file_path.exists(), f"Test file not found: {test_file_path}"

        # Initialize parser
        parser = Parser()
        chapters = parser.parse_epub(test_file_path)

        # Verify the data structure
        assert isinstance(chapters, list), "chapters should be a list"
        assert len(chapters) > 0, "should have at least one chapter"

        for i, chapter in enumerate(chapters):
            assert isinstance(chapter, tuple), f"chapter {i} should be a tuple"
            assert len(chapter) == 2, f"chapter {i} should have exactly 2 elements"

            title, text = chapter
            assert isinstance(title, str), f"chapter {i} title should be a string"
            assert isinstance(text, str), f"chapter {i} text should be a string"
            assert len(title) > 0, f"chapter {i} title should not be empty"
            # Skip text length check for cover/title pages
            if "cover" not in title.lower() and "title" not in title.lower():
                assert len(text) > 0, f"chapter {i} text should not be empty"

    def test_bad_path_handling(self):
        """Test handling of various bad path scenarios."""
        from vivre.parser import Parser

        parser = Parser()

        # Test with None path
        with pytest.raises(ValueError, match="File path cannot be None"):
            parser.load_epub(None)

        # Test with empty string path
        with pytest.raises(ValueError, match="File path cannot be empty"):
            parser.load_epub("")

        # Test with whitespace-only path
        with pytest.raises(ValueError, match="File path cannot be empty"):
            parser.load_epub("   ")

        # Test with path containing null bytes
        with pytest.raises(ValueError, match="File path contains invalid characters"):
            parser.load_epub("file\x00name.epub")

        # Test with path containing control characters
        with pytest.raises(ValueError, match="File path contains invalid characters"):
            parser.load_epub("file\nname.epub")

        # Test with relative path that doesn't exist
        with pytest.raises(FileNotFoundError, match="EPUB file not found"):
            parser.load_epub(Path("./nonexistent.epub"))

        # Test with absolute path that doesn't exist
        import tempfile

        temp_dir = tempfile.mkdtemp()
        try:
            nonexistent_path = Path(temp_dir) / "nonexistent.epub"
            with pytest.raises(FileNotFoundError, match="EPUB file not found"):
                parser.load_epub(nonexistent_path)
        finally:
            import shutil

            shutil.rmtree(temp_dir)

    def test_corrupted_file_handling(self):
        """Test handling of corrupted and malformed files."""
        import tempfile
        import zipfile

        from vivre.parser import Parser

        parser = Parser()

        # Test with completely empty file
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            temp_file.write(b"")
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

        # Test with file that's too small to be a ZIP
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            temp_file.write(b"PK\x03\x04")  # Only ZIP header, no content
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

        # Test with corrupted ZIP file (valid header but corrupted content)
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            # Create a ZIP file with corrupted content
            with zipfile.ZipFile(temp_file, "w") as zip_file:
                zip_file.writestr("test.txt", "Hello World")

            # Corrupt the file by truncating it
            temp_file.truncate(50)  # Truncate to corrupt the ZIP structure
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.parse_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

        # Test with ZIP file that's not an EPUB (missing required files)
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            with zipfile.ZipFile(temp_file, "w") as zip_file:
                zip_file.writestr("random.txt", "This is not an EPUB")
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.parse_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

    def test_non_epub_file_handling(self):
        """Test handling of files that are not EPUBs."""
        import tempfile

        from vivre.parser import Parser

        parser = Parser()

        # Test with text file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"This is a text file, not an EPUB")
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

        # Test with PDF file (different magic number)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(b"%PDF-1.4\nThis is a PDF file")
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

        # Test with image file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file.write(b"\xff\xd8\xff\xe0")  # JPEG magic number
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

        # Test with executable file
        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_file:
            temp_file.write(b"MZ")  # DOS executable magic number
            temp_file_path = Path(temp_file.name)

        try:
            with pytest.raises(ValueError, match="File is not a valid EPUB"):
                parser.load_epub(temp_file_path)
        finally:
            temp_file_path.unlink()

    def test_file_permission_handling(self):
        """Test handling of file permission issues."""
        import os
        import tempfile

        from vivre.parser import Parser

        parser = Parser()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
            temp_file.write(b"PK\x03\x04")  # Minimal ZIP header
            temp_file_path = Path(temp_file.name)

        try:
            # Make file unreadable
            os.chmod(temp_file_path, 0o000)

            with pytest.raises(ValueError, match="EPUB file is not readable"):
                parser.load_epub(temp_file_path)
        finally:
            # Restore permissions and clean up
            os.chmod(temp_file_path, 0o644)
            temp_file_path.unlink()

    def test_malicious_path_handling(self):
        """Test handling of potentially malicious paths."""
        from vivre.parser import Parser

        parser = Parser()

        # Test with path traversal attempts
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
        ]

        for malicious_path in malicious_paths:
            with pytest.raises((FileNotFoundError, ValueError)):
                parser.load_epub(Path(malicious_path))

        # Test with extremely long path
        long_path = "a" * 1000 + ".epub"
        with pytest.raises((FileNotFoundError, OSError)):
            parser.load_epub(Path(long_path))

    def test_parse_epub_with_bad_paths(self):
        """Test parse_epub method with various bad path scenarios."""
        from vivre.parser import Parser

        parser = Parser()

        # Test with None path
        with pytest.raises(ValueError, match="File path cannot be None"):
            parser.parse_epub(None)

        # Test with empty string path
        with pytest.raises(ValueError, match="File path cannot be empty"):
            parser.parse_epub("")

        # Test with non-existent file
        with pytest.raises(FileNotFoundError, match="EPUB file not found"):
            parser.parse_epub(Path("nonexistent.epub"))

        # Test with directory
        with pytest.raises(ValueError, match="Path is not a file"):
            parser.parse_epub(Path(__file__).parent / "data")

    def test_invalid_path_type_handling(self):
        """Test handling of invalid path types."""
        from vivre.parser import Parser

        parser = Parser()

        # Test with invalid path types
        invalid_paths = [
            123,  # integer
            3.14,  # float
            True,  # boolean
            [],  # list
            {},  # dict
            set(),  # set
        ]

        for invalid_path in invalid_paths:
            with pytest.raises(
                ValueError, match="File path must be a string or Path object"
            ):
                parser.load_epub(invalid_path)

        for invalid_path in invalid_paths:
            with pytest.raises(
                ValueError, match="File path must be a string or Path object"
            ):
                parser.parse_epub(invalid_path)

    def test_parse_percy_jackson_english(self):
        """Test parsing the English Percy Jackson EPUB file."""
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

        # Initialize parser and parse EPUB
        parser = Parser()
        chapters = parser.parse_epub(test_file_path)

        # Verify the structure and content
        assert isinstance(chapters, list), "chapters should be a list"
        assert len(chapters) > 0, "should extract at least one chapter"

        # Check chapter titles and content
        for i, (title, text) in enumerate(chapters):
            assert isinstance(title, str), f"chapter {i} title should be a string"
            assert isinstance(text, str), f"chapter {i} text should be a string"
            assert len(title) > 0, f"chapter {i} title should not be empty"
            assert len(text) > 0, f"chapter {i} text should not be empty"

            # Verify the text contains story content (not just metadata)
            assert len(text) > 100, f"chapter {i} should have substantial text content"

            print(f"Chapter {i+1}: {title}")
            print(f"Text length: {len(text)} characters")
            print(f"Text preview: {text[:100]}...")

    def test_parse_percy_jackson_spanish(self):
        """Test parsing the Spanish Percy Jackson EPUB file."""
        from vivre.parser import Parser

        # Get path to Spanish test EPUB file
        test_file_path = (
            Path(__file__).parent / "data" / "El ladrón del rayo - Rick Riordan.epub"
        )

        # Verify test file exists
        assert test_file_path.exists(), f"Test file not found: {test_file_path}"
        assert test_file_path.is_file(), f"Path is not a file: {test_file_path}"

        # Initialize parser and parse EPUB
        parser = Parser()
        chapters = parser.parse_epub(test_file_path)

        # Verify the structure and content
        assert isinstance(chapters, list), "chapters should be a list"
        assert len(chapters) > 0, "should extract at least one chapter"

        # Check chapter titles and content
        for i, (title, text) in enumerate(chapters):
            assert isinstance(title, str), f"chapter {i} title should be a string"
            assert isinstance(text, str), f"chapter {i} text should be a string"
            assert len(title) > 0, f"chapter {i} title should not be empty"
            assert len(text) > 0, f"chapter {i} text should not be empty"

            # Verify the text contains story content (not just metadata)
            assert len(text) > 100, f"chapter {i} should have substantial text content"

            print(f"Chapter {i+1}: {title}")
            print(f"Text length: {len(text)} characters")
            print(f"Text preview: {text[:100]}...")

    def test_filter_non_story_content(self):
        """Test that the parser correctly filters out non-story content."""
        from vivre.parser import Parser

        parser = Parser()

        # Test various non-story content titles that should be filtered out
        non_story_titles = [
            "Cover",
            "Title Page",
            "Front Cover",
            "Back Cover",
            "Acknowledgements",
            "Acknowledgments",
            "Table of Contents",
            "Contents",
            "Copyright",
            "Legal Notice",
            "About the Author",
            "Author Biography",
            "Translator's Note",
            "Preface",
            "Foreword",
            "Introduction",
            "Prologue",
            "Epilogue",
            "Afterword",
            "Appendix",
            "Index",
            "Bibliography",
            "References",
            "Glossary",
            "Credits",
            "Dedication",
        ]

        for title in non_story_titles:
            assert (
                parser._is_non_story_content(title, "test.xhtml") is True
            ), f"Should filter out: {title}"

        # Test story content titles that should NOT be filtered out
        story_titles = [
            "Chapter 1",
            "Chapter 1 - A Secret Code",
            "1. Código secreto",
            "The Beginning",
            "A New Adventure",
            "The Mystery Deepens",
            "The Final Battle",
            "Percy Jackson",
            "The Lightning Thief",
            "Part One",
            "Section 1",
        ]

        for title in story_titles:
            assert (
                parser._is_non_story_content(title, "chapter1.xhtml") is False
            ), f"Should NOT filter out: {title}"

    def test_epub_content_filtering_integration(self):
        """Test that EPUB parsing correctly filters non-story content in real files."""
        from vivre.parser import Parser

        # Test with both Percy Jackson files
        test_files = [
            ("Percy Jackson 1 - The Lightning Thief - Riordan, Rick.epub", 1),
            ("El ladrón del rayo - Rick Riordan.epub", 1),
        ]

        for filename, expected_chapters in test_files:
            test_file_path = Path(__file__).parent / "data" / filename

            # Verify test file exists
            assert test_file_path.exists(), f"Test file not found: {test_file_path}"

            # Initialize parser and parse EPUB
            parser = Parser()
            chapters = parser.parse_epub(test_file_path)

            # Verify we get at least one chapter
            assert (
                len(chapters) >= expected_chapters
            ), f"Expected at least {expected_chapters} chapter for {filename}, got {len(chapters)}"

            # Verify all chapters have substantial content
            for i, (title, text) in enumerate(chapters):
                assert (
                    len(title) > 0
                ), f"Chapter {i} title should not be empty in {filename}"
                assert (
                    len(text) > 100
                ), f"Chapter {i} should have substantial text in {filename}"

                # Verify the title doesn't contain non-story keywords
                title_lower = title.lower()
                non_story_keywords = [
                    "cover",
                    "title",
                    "acknowledgement",
                    "contents",
                    "copyright",
                    "about the author",
                    "translator",
                    "preface",
                    "epilogue",
                ]

                for keyword in non_story_keywords:
                    assert (
                        keyword not in title_lower
                    ), f"Chapter title '{title}' should not contain '{keyword}' in {filename}"

            print(
                f"✓ {filename}: Extracted {len(chapters)} story chapters successfully"
            )
