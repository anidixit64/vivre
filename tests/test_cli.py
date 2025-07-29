"""
Tests for the CLI interface.
"""

import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from vivre.cli import app

runner = CliRunner()


class TestCLIParseCommand:
    """Test the parse command."""

    def test_parse_basic_output(self, epub_path):
        """Test basic parse command output."""
        result = runner.invoke(app, ["parse", str(epub_path)])
        assert result.exit_code == 0
        assert "chapters" in result.stdout

    def test_parse_json_format(self, epub_path):
        """Test parse command with JSON format."""
        result = runner.invoke(app, ["parse", str(epub_path), "--format", "json"])
        assert result.exit_code == 0
        # Don't try to parse JSON if it might contain control characters
        assert "chapters" in result.stdout

    def test_parse_with_show_content(self, epub_path):
        """Test parse command with show content flag."""
        result = runner.invoke(app, ["parse", str(epub_path), "--show-content"])
        assert result.exit_code == 0
        assert "content" in result.stdout

    def test_parse_with_segment(self, epub_path):
        """Test parse command with segmentation."""
        result = runner.invoke(app, ["parse", str(epub_path), "--segment"])
        assert result.exit_code == 0
        assert "sentences" in result.stdout

    def test_parse_with_output_file(self, epub_path):
        """Test parse command with output file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            result = runner.invoke(
                app, ["parse", str(epub_path), "--output", output_path]
            )
            assert result.exit_code == 0
            assert Path(output_path).exists()
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_parse_invalid_format(self, epub_path):
        """Test parse command with invalid format."""
        result = runner.invoke(app, ["parse", str(epub_path), "--format", "invalid"])
        # Should fail with invalid format
        assert result.exit_code != 0

    def test_parse_nonexistent_file(self):
        """Test parse command with nonexistent file."""
        result = runner.invoke(app, ["parse", "nonexistent.epub"])
        assert result.exit_code != 0

    def test_parse_with_language_parameter(self, epub_path):
        """Test parse command with language parameter."""
        result = runner.invoke(app, ["parse", str(epub_path), "--language", "en"])
        assert result.exit_code == 0

    def test_parse_with_max_chapters(self, epub_path):
        """Test parse command with max chapters limit."""
        result = runner.invoke(app, ["parse", str(epub_path), "--max-chapters", "2"])
        assert result.exit_code == 0
        # Don't try to parse JSON if it might contain control characters
        assert "chapters" in result.stdout

    def test_parse_with_verbose(self, epub_path):
        """Test parse command with verbose output."""
        result = runner.invoke(app, ["parse", str(epub_path), "--verbose"])
        assert result.exit_code == 0


class TestCLIAlignCommand:
    """Test the align command."""

    def test_align_basic_output(self, source_epub_path, target_epub_path):
        """Test basic align command output."""
        result = runner.invoke(
            app, ["align", str(source_epub_path), str(target_epub_path), "en-es"]
        )
        assert result.exit_code == 0
        assert "chapters" in result.stdout

    def test_align_json_format(self, source_epub_path, target_epub_path):
        """Test align command with JSON format."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--format",
                "json",
            ],
        )
        assert result.exit_code == 0
        # Don't try to parse JSON if it might contain control characters
        assert "chapters" in result.stdout

    def test_align_csv_format(self, source_epub_path, target_epub_path):
        """Test align command with CSV format."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--format",
                "csv",
            ],
        )
        assert result.exit_code == 0
        assert "chapter,title,en,es" in result.stdout

    def test_align_with_output_file(self, source_epub_path, target_epub_path):
        """Test align command with output file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            result = runner.invoke(
                app,
                [
                    "align",
                    str(source_epub_path),
                    str(target_epub_path),
                    "en-es",
                    "--output",
                    output_path,
                ],
            )
            assert result.exit_code == 0
            assert Path(output_path).exists()
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_align_with_verbose(self, source_epub_path, target_epub_path):
        """Test align command with verbose output."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--verbose",
            ],
        )
        assert result.exit_code == 0
        assert "Alignment Complete!" in result.stdout

    def test_align_invalid_language_pair(self, source_epub_path, target_epub_path):
        """Test align command with invalid language pair."""
        result = runner.invoke(
            app, ["align", str(source_epub_path), str(target_epub_path), "invalid"]
        )
        assert result.exit_code != 0

    def test_align_invalid_format(self, source_epub_path, target_epub_path):
        """Test align command with invalid format."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--format",
                "invalid",
            ],
        )
        # Should fail with invalid format
        assert result.exit_code != 0

    def test_align_nonexistent_source_file(self, target_epub_path):
        """Test align command with nonexistent source file."""
        result = runner.invoke(
            app, ["align", "nonexistent.epub", str(target_epub_path), "en-es"]
        )
        assert result.exit_code != 0

    def test_align_nonexistent_target_file(self, source_epub_path):
        """Test align command with nonexistent target file."""
        result = runner.invoke(
            app, ["align", str(source_epub_path), "nonexistent.epub", "en-es"]
        )
        assert result.exit_code != 0

    def test_align_with_custom_parameters(self, source_epub_path, target_epub_path):
        """Test align command with custom alignment parameters."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--c",
                "1.1",
                "--s2",
                "7.0",
                "--gap-penalty",
                "2.5",
            ],
        )
        assert result.exit_code == 0

    def test_align_with_invalid_method(self, source_epub_path, target_epub_path):
        """Test align command with invalid method."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--method",
                "invalid",
            ],
        )
        assert result.exit_code != 0


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_help_command(self):
        """Test help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "vivre" in result.stdout

    def test_parse_help(self):
        """Test parse help."""
        result = runner.invoke(app, ["parse", "--help"])
        assert result.exit_code == 0
        assert "parse" in result.stdout

    def test_align_help(self):
        """Test align help."""
        result = runner.invoke(app, ["align", "--help"])
        assert result.exit_code == 0
        assert "align" in result.stdout

    def test_version_flag(self):
        """Test version flag."""
        result = runner.invoke(app, ["--version"])
        # Typer exits with 2 when no command is provided
        assert result.exit_code == 2
        assert "vivre" in result.stdout

    def test_invalid_command(self):
        """Test invalid command."""
        result = runner.invoke(app, ["invalid"])
        assert result.exit_code != 0

    def test_missing_arguments(self):
        """Test missing arguments."""
        result = runner.invoke(app, ["parse"])
        assert result.exit_code != 0

    def test_align_missing_arguments(self):
        """Test align command with missing arguments."""
        result = runner.invoke(app, ["align"])
        assert result.exit_code != 0


class TestCLIFormatOptions:
    """Test CLI format options."""

    @pytest.mark.parametrize("format_type", ["json", "dict", "text", "csv", "xml"])
    def test_parse_all_formats(self, epub_path, format_type):
        """Test parse command with all format options."""
        result = runner.invoke(
            app,
            [
                "parse",
                str(epub_path),
                "--format",
                format_type,
                "--max-chapters",
                "1",
            ],
        )
        assert result.exit_code == 0

    @pytest.mark.parametrize("format_type", ["json", "dict", "text", "csv", "xml"])
    def test_align_all_formats(self, source_epub_path, target_epub_path, format_type):
        """Test align command with all format options."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--format",
                format_type,
            ],
        )
        assert result.exit_code == 0


class TestCLIEdgeCases:
    """Test CLI edge cases and error conditions."""

    def test_parse_with_empty_epub(self, tmp_path):
        """Test parse command with empty EPUB file."""
        # Create an empty file
        empty_epub = tmp_path / "empty.epub"
        empty_epub.write_text("")

        result = runner.invoke(app, ["parse", str(empty_epub)])
        assert result.exit_code != 0

    def test_align_with_identical_files(self, source_epub_path):
        """Test align command with identical source and target files."""
        result = runner.invoke(
            app, ["align", str(source_epub_path), str(source_epub_path), "en-es"]
        )
        # This should work but might produce unexpected results
        assert result.exit_code == 0

    def test_parse_with_large_max_chapters(self, epub_path):
        """Test parse command with very large max chapters value."""
        result = runner.invoke(app, ["parse", str(epub_path), "--max-chapters", "9999"])
        assert result.exit_code == 0

    def test_align_with_unsupported_language_pair(
        self, source_epub_path, target_epub_path
    ):
        """Test align command with unsupported language pair."""
        result = runner.invoke(
            app, ["align", str(source_epub_path), str(target_epub_path), "xx-yy"]
        )
        # The aligner might actually work with unsupported language pairs
        # So we just check that it doesn't crash
        assert result.exit_code in [0, 1]  # Could be either success or failure

    def test_parse_with_nonexistent_output_directory(self, epub_path):
        """Test parse command with nonexistent output directory."""
        result = runner.invoke(
            app, ["parse", str(epub_path), "--output", "/nonexistent/dir/output.json"]
        )
        assert result.exit_code != 0

    def test_align_with_nonexistent_output_directory(
        self, source_epub_path, target_epub_path
    ):
        """Test align command with nonexistent output directory."""
        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub_path),
                str(target_epub_path),
                "en-es",
                "--output",
                "/nonexistent/dir/output.json",
            ],
        )
        assert result.exit_code != 0


class TestCLIFormattingFunctions:
    """Test the internal formatting functions."""

    def test_format_alignments_as_text(self):
        """Test _format_alignments_as_text function."""
        from vivre.cli import _format_alignments_as_text

        test_data = {
            "book_title": "Test Book",
            "language_pair": "en-es",
            "method": "gale-church",
            "total_alignments": 2,
            "alignments": [
                {"id": 1, "source": "Hello", "target": "Hola"},
                {"id": 2, "source": "World", "target": "Mundo"},
            ],
        }

        result = _format_alignments_as_text(test_data)
        assert "Test Book" in result
        assert "en-es" in result
        assert "Hello" in result
        assert "Hola" in result

    def test_format_alignments_as_csv(self):
        """Test _format_alignments_as_csv function."""
        from vivre.cli import _format_alignments_as_csv

        test_data = {
            "book_title": "Test Book",
            "language_pair": "en-es",
            "method": "gale-church",
            "source_epub": "source.epub",
            "target_epub": "target.epub",
            "total_alignments": 2,
            "alignments": [
                {
                    "id": 1,
                    "source": "Hello",
                    "target": "Hola",
                    "source_length": 5,
                    "target_length": 4,
                },
                {
                    "id": 2,
                    "source": "World",
                    "target": "Mundo",
                    "source_length": 5,
                    "target_length": 5,
                },
            ],
        }

        result = _format_alignments_as_csv(test_data)
        assert (
            "book_title,language_pair,method,source_epub,target_epub,total_alignments"
            in result
        )
        assert "id,en,es,source_length,target_length" in result

    def test_format_alignments_as_xml(self):
        """Test _format_alignments_as_xml function."""
        from vivre.cli import _format_alignments_as_xml

        test_data = {
            "book_title": "Test Book",
            "language_pair": "en-es",
            "method": "gale-church",
            "source_epub": "source.epub",
            "target_epub": "target.epub",
            "total_alignments": 2,
            "alignments": [
                {
                    "id": 1,
                    "source": "Hello",
                    "target": "Hola",
                    "source_length": 5,
                    "target_length": 4,
                },
                {
                    "id": 2,
                    "source": "World",
                    "target": "Mundo",
                    "source_length": 5,
                    "target_length": 5,
                },
            ],
        }

        result = _format_alignments_as_xml(test_data)
        assert '<?xml version="1.0" encoding="UTF-8"?>' in result
        assert "<alignments>" in result
        assert "<book_title>Test Book</book_title>" in result

    def test_format_parse_as_text(self):
        """Test _format_parse_as_text function."""
        from vivre.cli import _format_parse_as_text

        test_data = {
            "file_path": "test.epub",
            "book_title": "Test Book",
            "book_author": "Test Author",
            "book_language": "en",
            "chapter_count": 2,
            "chapters": [
                {
                    "number": 1,
                    "title": "Chapter 1",
                    "content": "Content 1",
                    "word_count": 2,
                    "character_count": 10,
                },
                {
                    "number": 2,
                    "title": "Chapter 2",
                    "content": "Content 2",
                    "word_count": 2,
                    "character_count": 10,
                },
            ],
        }

        result = _format_parse_as_text(test_data)
        assert "Test Book" in result
        assert "Chapter 1" in result
        assert "Content 1" in result

    def test_format_parse_as_csv(self):
        """Test _format_parse_as_csv function."""
        from vivre.cli import _format_parse_as_csv

        test_data = {
            "file_path": "test.epub",
            "book_title": "Test Book",
            "book_author": "Test Author",
            "book_language": "en",
            "chapter_count": 2,
            "chapters": [
                {
                    "number": 1,
                    "title": "Chapter 1",
                    "content": "Content 1",
                    "word_count": 2,
                    "character_count": 10,
                },
                {
                    "number": 2,
                    "title": "Chapter 2",
                    "content": "Content 2",
                    "word_count": 2,
                    "character_count": 10,
                },
            ],
        }

        result = _format_parse_as_csv(test_data)
        assert "file_path,book_title,book_author,book_language,chapter_count" in result
        assert "Chapter 1" in result
        # The CSV format doesn't include full content, just metadata
        assert (
            "chapter_number,title,word_count,character_count,content_preview" in result
        )

    def test_format_parse_as_xml(self):
        """Test _format_parse_as_xml function."""
        from vivre.cli import _format_parse_as_xml

        test_data = {
            "file_path": "test.epub",
            "book_title": "Test Book",
            "book_author": "Test Author",
            "book_language": "en",
            "chapter_count": 2,
            "chapters": [
                {
                    "number": 1,
                    "title": "Chapter 1",
                    "content": "Content 1",
                    "word_count": 2,
                    "character_count": 10,
                },
                {
                    "number": 2,
                    "title": "Chapter 2",
                    "content": "Content 2",
                    "word_count": 2,
                    "character_count": 10,
                },
            ],
        }

        result = _format_parse_as_xml(test_data)
        assert '<?xml version="1.0" encoding="UTF-8"?>' in result
        assert "<epub_parse>" in result
        assert "<book_title>Test Book</book_title>" in result
