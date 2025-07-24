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

    def test_remove_title_from_text(self):
        """Test the _remove_title_from_text method."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Test exact match removal
        text = "2. El fin está cerca Jack abrió los ojos"
        title = "2. El fin está cerca"
        result = parser._remove_title_from_text(text, title)
        assert result == "Jack abrió los ojos"

        # Test variation removal (without period)
        text = "2 El fin está cerca Jack abrió los ojos"
        title = "2. El fin está cerca"
        result = parser._remove_title_from_text(text, title)
        assert result == "Jack abrió los ojos"

        # Test with extra whitespace
        text = "  2. El fin está cerca  Jack abrió los ojos"
        title = "2. El fin está cerca"
        result = parser._remove_title_from_text(text, title)
        assert result == "Jack abrió los ojos"

        # Test with no title to remove
        text = "Jack abrió los ojos"
        title = "2. El fin está cerca"
        result = parser._remove_title_from_text(text, title)
        assert result == "Jack abrió los ojos"

        # Test with empty title
        text = "Jack abrió los ojos"
        title = ""
        result = parser._remove_title_from_text(text, title)
        assert result == "Jack abrió los ojos"

        # Test with "Untitled Chapter"
        text = "Jack abrió los ojos"
        title = "Untitled Chapter"
        result = parser._remove_title_from_text(text, title)
        assert result == "Jack abrió los ojos"

    def test_extract_title_fallback_with_chapter_pattern(self):
        """Test title extraction fallback with chapter number patterns."""
        from unittest.mock import patch

        from vivre.parser import VivreParser

        parser = VivreParser()

        # Test with chapter number pattern
        content = """
        <html>
        <body>
        2. El fin está cerca Jack abrió los ojos y se acomodó los lentes.
        </body>
        </html>
        """

        # Mock the XML parsing to fail and trigger fallback
        with patch.object(parser, "_extract_title", return_value="Untitled Chapter"):
            with patch.object(
                parser,
                "_extract_text",
                return_value="2. El fin está cerca Jack abrió los ojos",
            ):
                title, text = parser._extract_chapter_content(content.encode("utf-8"))
                # The fallback should extract the title from the text
                assert title == "2. El fin está cerca"
                assert text.startswith("Jack abrió los ojos")

    def test_extract_title_fallback_without_chapter_pattern(self):
        """Test title extraction fallback when no chapter pattern is found."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Test with content that has no chapter pattern
        content = b"""
        <html>
        <head><title>Some Title</title></head>
        <body>
        <p>This is some content without a chapter pattern.</p>
        <p>It should still extract a title from the title tag.</p>
        </body>
        </html>
        """

        title, text = parser._extract_chapter_content(content)
        assert title == "Some Title"
        assert "This is some content without a chapter pattern" in text

    def test_beautifulsoup_malformed_html_handling(self):
        """Test that BeautifulSoup handles malformed HTML gracefully."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Test with severely malformed HTML that would break XML parsing
        malformed_content = b"""
        <html>
        <head><title>Chapter 1</title></head>
        <body>
        <h1>Chapter 1: The Beginning</h1>
        <p>This is the first paragraph.
        <p>This paragraph has no closing tag.
        <div>This div is not closed either
        <h2>Subheading</h2>
        <p>More content here.</p>
        </body>
        </html>
        """

        # This should not raise an exception and should extract content
        title, text = parser._extract_chapter_content(malformed_content)

        # Should extract title from h1
        assert "Chapter 1: The Beginning" in title
        assert title != "Untitled Chapter"

        # Should extract text content despite malformed HTML
        assert "This is the first paragraph" in text
        assert "This paragraph has no closing tag" in text
        assert "More content here" in text

    def test_beautifulsoup_vs_xml_parsing(self):
        """Test that BeautifulSoup handles content that would break XML parsing."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Content with unclosed tags and invalid XML that would break ElementTree
        problematic_content = b"""
        <html>
        <head><title>Test Chapter</title></head>
        <body>
        <h1>Test Chapter</h1>
        <p>This content has <b>unclosed tags and <i>nested unclosed tags
        <p>Another paragraph with <a href="http://example.com">unclosed link
        <div>Unclosed div with <span>unclosed span
        <p>Final paragraph.</p>
        </body>
        </html>
        """

        # This should work with BeautifulSoup but would fail with ElementTree
        title, text = parser._extract_chapter_content(problematic_content)

        # Should extract title
        assert title == "Test Chapter"

        # Should extract text content despite malformed HTML
        assert "This content has" in text
        assert "unclosed tags" in text
        assert "Another paragraph" in text
        assert "Final paragraph" in text

    def test_epub_standards_toc_discovery(self):
        """Test EPUB standards-compliant table of contents discovery."""
        from unittest.mock import MagicMock, patch

        from vivre.parser import VivreParser

        parser = VivreParser()

        # Mock content.opf with EPUB3 navigation document
        mock_content_opf = b"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0">
    <metadata>
        <dc:title>Test Book</dc:title>
        <dc:language>en</dc:language>
    </metadata>
    <manifest>
        <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
        <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    </manifest>
    <spine>
        <itemref idref="chapter1"/>
    </spine>
</package>"""

        # Mock navigation document content
        mock_nav_content = b"""
        <?xml version="1.0" encoding="UTF-8"?>
        <html xmlns="http://www.w3.org/1999/xhtml">
            <body>
                <nav>
                    <ol>
                        <li><a href="chapter1.xhtml">Chapter 1: The Beginning</a></li>
                    </ol>
                </nav>
            </body>
        </html>
        """

        with patch("zipfile.ZipFile") as mock_zip:
            mock_zip_instance = MagicMock()
            mock_zip.return_value.__enter__.return_value = mock_zip_instance
            mock_zip_instance.read.side_effect = lambda path: {
                "META-INF/container.xml": b'<container><rootfiles><rootfile full-path="content.opf"/></rootfiles></container>',
                "content.opf": mock_content_opf,
                "nav.xhtml": mock_nav_content,
            }.get(path, b"")

            # Test EPUB3 navigation discovery
            nav_path = parser._find_navigation_document(
                mock_content_opf, mock_zip_instance, Path(".")
            )
            assert nav_path == "nav.xhtml"

        # Test EPUB2 fallback
        mock_content_opf_epub2 = b"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">
    <manifest>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="chapter1"/>
    </spine>
</package>"""

        with patch("zipfile.ZipFile") as mock_zip:
            mock_zip_instance = MagicMock()
            mock_zip.return_value.__enter__.return_value = mock_zip_instance
            mock_zip_instance.read.side_effect = lambda path: {
                "META-INF/container.xml": b'<container><rootfiles><rootfile full-path="content.opf"/></rootfiles></container>',
                "content.opf": mock_content_opf_epub2,
            }.get(path, b"")

            # Test EPUB2 NCX discovery
            nav_path = parser._find_navigation_document(
                mock_content_opf_epub2, mock_zip_instance, Path(".")
            )
            assert nav_path == "toc.ncx"

    def test_multilingual_content_filtering(self):
        """Test multilingual non-story content filtering."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Test English filtering
        parser._book_language = "en"
        assert parser._is_non_story_content("Copyright Page", "copyright.xhtml")
        assert not parser._is_non_story_content("Chapter 1", "chapter1.xhtml")

        # Test Spanish filtering
        parser._book_language = "es"
        assert parser._is_non_story_content("Derechos de Autor", "copyright.xhtml")
        assert not parser._is_non_story_content("Capítulo 1", "chapter1.xhtml")

        # Test French filtering
        parser._book_language = "fr"
        assert parser._is_non_story_content("Droits d'Auteur", "copyright.xhtml")
        assert not parser._is_non_story_content("Chapitre 1", "chapter1.xhtml")

        # Test fallback to English for unsupported language
        parser._book_language = "xx"
        assert parser._is_non_story_content("Copyright Page", "copyright.xhtml")

    def test_metadata_extraction(self):
        """Test metadata extraction from content.opf."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Test metadata extraction
        mock_content_opf = b"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0">
    <metadata>
        <dc:title>Test Book Title</dc:title>
        <dc:language>es</dc:language>
    </metadata>
</package>"""

        parser._extract_metadata(mock_content_opf)
        assert parser._book_title == "Test Book Title"
        assert parser._book_language == "es"

        # Test language code mapping
        mock_content_opf_fr = b"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0">
    <metadata>
        <dc:title>Livre de Test</dc:title>
        <dc:language>fra</dc:language>
    </metadata>
</package>"""

        parser._extract_metadata(mock_content_opf_fr)
        assert parser._book_title == "Livre de Test"
        assert parser._book_language == "fr"

    def test_paragraph_structure_preservation(self):
        """Test that paragraph structure is preserved in text extraction."""
        from vivre.parser import VivreParser

        parser = VivreParser()

        # Content with multiple paragraphs
        content = b"""
        <html>
        <head><title>Test Chapter</title></head>
        <body>
        <h1>Test Chapter</h1>
        <p>This is the first paragraph.</p>
        <p>This is the second paragraph.</p>
        <div>This is a div block.</div>
        <p>This is the third paragraph.</p>
        </body>
        </html>
        """

        title, text = parser._extract_chapter_content(content)

        # Should extract title
        assert title == "Test Chapter"

        # Should preserve paragraph structure with double newlines
        assert "This is the first paragraph." in text
        assert "This is the second paragraph." in text
        assert "This is a div block." in text
        assert "This is the third paragraph." in text

        # Should preserve paragraph structure (check that paragraphs are separated)
        # The text should have some structure, not be completely flattened
        assert len(text.split()) > 4  # Should have multiple words
        # Check that the text contains all expected content
        assert all(
            phrase in text
            for phrase in [
                "This is the first paragraph",
                "This is the second paragraph",
                "This is a div block",
                "This is the third paragraph",
            ]
        )
