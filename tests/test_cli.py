"""
Tests for the CLI interface using Typer's CliRunner.
"""

import json
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from vivre.cli import app

# Create CliRunner instance
runner = CliRunner()


class TestCLIParseCommand:
    """Test the 'vivre parse' command."""

    def test_parse_basic_output(self):
        """Test that vivre parse produces expected stdout."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        result = runner.invoke(app, ["parse", str(epub_path)])

        assert result.exit_code == 0
        assert "file_path" in result.stdout
        assert "book_title" in result.stdout
        assert "chapter_count" in result.stdout
        assert "chapters" in result.stdout

    def test_parse_json_format(self):
        """Test that vivre parse --format json produces expected stdout."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        result = runner.invoke(app, ["parse", str(epub_path), "--format", "json"])

        assert result.exit_code == 0

        # Check that output contains expected JSON structure
        assert "file_path" in result.stdout
        assert "book_title" in result.stdout
        assert "chapter_count" in result.stdout
        assert "chapters" in result.stdout
        assert "[" in result.stdout  # Should contain array brackets
        assert "{" in result.stdout  # Should contain object brackets

    def test_parse_with_show_content(self):
        """Test parse command with --show-content flag."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        result = runner.invoke(
            app, ["parse", str(epub_path), "--show-content", "--max-chapters", "1"]
        )

        assert result.exit_code == 0
        assert "content" in result.stdout

    def test_parse_with_segment(self):
        """Test parse command with --segment flag."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        result = runner.invoke(
            app, ["parse", str(epub_path), "--segment", "--max-chapters", "1"]
        )

        assert result.exit_code == 0
        # Should contain sentence segmentation data
        assert "sentences" in result.stdout

    def test_parse_with_output_file(self):
        """Test parse command with --output flag."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            result = runner.invoke(
                app, ["parse", str(epub_path), "--output", output_path]
            )

            assert result.exit_code == 0
            assert "Results saved to:" in result.stdout

            # Verify the output file was created and contains valid JSON
            with open(output_path, "r") as f:
                data = json.load(f)
                assert "file_path" in data
                assert "book_title" in data

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_parse_invalid_format(self):
        """Test that invalid format produces helpful error message."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        result = runner.invoke(
            app, ["parse", str(epub_path), "--format", "invalid_format"]
        )

        assert result.exit_code != 0
        assert "Invalid format" in result.stdout
        assert "json" in result.stdout or "dict" in result.stdout

    def test_parse_nonexistent_file(self):
        """Test that nonexistent file produces error."""
        result = runner.invoke(app, ["parse", "nonexistent.epub"])

        assert result.exit_code != 0
        assert "Error" in result.stdout or "File" in result.stdout


class TestCLIAlignCommand:
    """Test the 'vivre align' command."""

    def test_align_basic_output(self):
        """Test that vivre align produces expected stdout."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app, ["align", str(source_epub), str(target_epub), "en-es"]
        )

        assert result.exit_code == 0
        assert "book_title" in result.stdout
        assert "language_pair" in result.stdout
        assert "alignments" in result.stdout

    def test_align_json_format(self):
        """Test that vivre align --format json produces expected stdout."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app,
            ["align", str(source_epub), str(target_epub), "en-es", "--format", "json"],
        )

        assert result.exit_code == 0

        # Check that output contains expected JSON structure
        assert "book_title" in result.stdout
        assert "language_pair" in result.stdout
        assert "chapters" in result.stdout
        assert "alignments" in result.stdout
        assert "{" in result.stdout  # Should contain object brackets

    def test_align_csv_format(self):
        """Test align command with CSV format."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app,
            ["align", str(source_epub), str(target_epub), "en-es", "--format", "csv"],
        )

        assert result.exit_code == 0
        assert "chapter" in result.stdout
        assert "title" in result.stdout
        assert "en" in result.stdout
        assert "es" in result.stdout
        assert "," in result.stdout  # CSV should contain commas

    def test_align_with_output_file(self):
        """Test align command with --output flag."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            result = runner.invoke(
                app,
                [
                    "align",
                    str(source_epub),
                    str(target_epub),
                    "en-es",
                    "--output",
                    output_path,
                ],
            )

            assert result.exit_code == 0
            assert "Results saved to:" in result.stdout

            # Verify the output file was created and contains valid JSON
            with open(output_path, "r") as f:
                data = json.load(f)
                assert "book_title" in data
                assert "language_pair" in data

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_align_with_verbose(self):
        """Test align command with --verbose flag."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub),
                str(target_epub),
                "en-es",
                "--verbose",
            ],
        )

        assert result.exit_code == 0
        assert "Alignment Configuration" in result.stdout
        assert "Summary" in result.stdout

    def test_align_invalid_language_pair(self):
        """Test that invalid language pair produces error."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app, ["align", str(source_epub), str(target_epub), "invalid"]
        )

        assert result.exit_code != 0
        assert "Invalid language pair" in result.stdout
        assert "en-fr" in result.stdout or "es-en" in result.stdout

    def test_align_invalid_format(self):
        """Test that invalid format produces error."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub),
                str(target_epub),
                "en-es",
                "--format",
                "invalid_format",
            ],
        )

        assert result.exit_code != 0
        assert "Invalid format" in result.stdout

    def test_align_nonexistent_source_file(self):
        """Test that nonexistent source file produces error."""
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app, ["align", "nonexistent.epub", str(target_epub), "en-es"]
        )

        assert result.exit_code != 0
        assert "Error" in result.stdout or "File" in result.stdout

    def test_align_nonexistent_target_file(self):
        """Test that nonexistent target file produces error."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

        result = runner.invoke(
            app, ["align", str(source_epub), "nonexistent.epub", "en-es"]
        )

        assert result.exit_code != 0
        assert "Error" in result.stdout or "File" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling and help messages."""

    def test_help_command(self):
        """Test that --help produces helpful output."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "vivre" in result.stdout
        assert "parse" in result.stdout
        assert "align" in result.stdout

    def test_parse_help(self):
        """Test that parse --help produces helpful output."""
        result = runner.invoke(app, ["parse", "--help"])

        assert result.exit_code == 0
        # Check for key elements that should be in the help output
        assert "epub_path" in result.stdout or "EPUB_PATH" in result.stdout
        assert "format" in result.stdout
        assert "verbose" in result.stdout

    def test_align_help(self):
        """Test that align --help produces helpful output."""
        result = runner.invoke(app, ["align", "--help"])

        assert result.exit_code == 0
        # Check for key elements that should be in the help output
        assert "source_epub" in result.stdout or "SOURCE_EPUB" in result.stdout
        assert "target_epub" in result.stdout or "TARGET_EPUB" in result.stdout
        assert "language_pair" in result.stdout or "LANGUAGE_PAIR" in result.stdout

    def test_version_flag(self):
        """Test that --version shows version."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 2  # Typer exits with 2 when no command is provided
        assert "vivre" in result.stdout
        assert "0.1.0" in result.stdout

    def test_invalid_command(self):
        """Test that invalid command produces error."""
        result = runner.invoke(app, ["invalid-command"])

        assert result.exit_code != 0
        assert "Error" in result.stdout

    def test_missing_arguments(self):
        """Test that missing required arguments produces error."""
        result = runner.invoke(app, ["parse"])

        assert result.exit_code != 0
        assert "Error" in result.stdout

        result = runner.invoke(app, ["align"])

        assert result.exit_code != 0
        assert "Error" in result.stdout


class TestCLIFormatOptions:
    """Test different output formats for CLI commands."""

    @pytest.mark.parametrize("format_type", ["json", "dict", "text", "csv", "xml"])
    def test_parse_all_formats(self, format_type):
        """Test parse command with all available formats."""
        epub_path = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )

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

        assert result.exit_code == 0, f"Format {format_type} failed"
        assert len(result.stdout) > 0, f"Format {format_type} produced empty output"

        # Test specific format characteristics
        if format_type == "json":
            # Should contain JSON structure
            assert "{" in result.stdout
            assert "}" in result.stdout

        elif format_type == "csv":
            # Should contain commas
            assert "," in result.stdout

        elif format_type == "xml":
            # Should contain XML tags
            assert "<" in result.stdout and ">" in result.stdout

    @pytest.mark.parametrize("format_type", ["json", "dict", "text", "csv", "xml"])
    def test_align_all_formats(self, format_type):
        """Test align command with all available formats."""
        source_epub = (
            Path(__file__).parent
            / "data"
            / "Vacation Under the Volcano - Mary Pope Osborne.epub"
        )
        target_epub = (
            Path(__file__).parent / "data" / "Vacaciones al pie de un volcán.epub"
        )

        result = runner.invoke(
            app,
            [
                "align",
                str(source_epub),
                str(target_epub),
                "en-es",
                "--format",
                format_type,
            ],
        )

        assert result.exit_code == 0, f"Format {format_type} failed"
        assert len(result.stdout) > 0, f"Format {format_type} produced empty output"

        # Test specific format characteristics
        if format_type == "json":
            # Should contain JSON structure
            assert "{" in result.stdout
            assert "}" in result.stdout

        elif format_type == "csv":
            # Should contain commas
            assert "," in result.stdout

        elif format_type == "xml":
            # Should contain XML tags
            assert "<" in result.stdout and ">" in result.stdout
