"""
Command-line interface for the vivre library.

This module provides a CLI for common tasks like reading EPUB files
and aligning parallel texts.
"""

import json
from pathlib import Path
from typing import Optional, Union

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from .api import align as align_api
from .api import read
from .integration import VivrePipeline
from .parser import VivreParser

# Create Typer app and console
app = typer.Typer(
    name="vivre",
    help="A library for processing parallel texts",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def align(
    source_epub: Path = typer.Argument(
        ...,
        help="Path to source language EPUB file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    target_epub: Path = typer.Argument(
        ...,
        help="Path to target language EPUB file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    method: str = typer.Option(
        "gale-church",
        "--method",
        "-m",
        help="Alignment method to use",
        case_sensitive=False,
    ),
    format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format",
        case_sensitive=False,
    ),
    language_pair: Optional[str] = typer.Option(
        None,
        "--language-pair",
        "-l",
        help="Language pair code (e.g., 'en-es', auto-detected if not specified)",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: stdout)",
        file_okay=True,
        dir_okay=False,
    ),
    c: Optional[float] = typer.Option(
        None,
        "--c",
        help="Gale-Church alignment parameter c",
    ),
    s2: Optional[float] = typer.Option(
        None,
        "--s2",
        help="Gale-Church alignment parameter s2",
    ),
    gap_penalty: Optional[float] = typer.Option(
        None,
        "--gap-penalty",
        help="Gale-Church gap penalty parameter",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed progress and statistics",
    ),
) -> None:
    """
    Align two EPUB files using the complete pipeline.

    This command orchestrates the entire pipeline: parsing both EPUB files,
    segmenting text into sentences, and aligning sentences using the specified method.

    Examples:
        vivre align english.epub spanish.epub
        vivre align book1.epub book2.epub --method gale-church --format json
        vivre align book1.epub book2.epub --language-pair en-fr --format csv
        vivre align book1.epub book2.epub --c 1.1 --s2 7.0 --gap-penalty 2.5
    """
    try:
        # Validate method
        if method.lower() != "gale-church":
            console.print(
                f"[red]Invalid method:[/red] {method}. "
                f"Only 'gale-church' is currently supported."
            )
            raise typer.Exit(1)

        # Validate format
        if format.lower() not in ["json", "dict", "text", "csv", "xml"]:
            console.print(
                f"[red]Invalid format:[/red] {format}. "
                f"Use 'json', 'dict', 'text', 'csv', or 'xml'"
            )
            raise typer.Exit(1)

        # Auto-detect language pair if not provided
        if language_pair is None:
            from .api import _detect_language_from_filename

            source_lang = _detect_language_from_filename(source_epub)
            target_lang = _detect_language_from_filename(target_epub)
            language_pair = f"{source_lang}-{target_lang}"
            if verbose:
                console.print(
                    f"[yellow]Auto-detected language pair:[/yellow] {language_pair}"
                )

        # Prepare pipeline parameters
        pipeline_kwargs = {}
        if c is not None:
            pipeline_kwargs["c"] = c
        if s2 is not None:
            pipeline_kwargs["s2"] = s2
        if gap_penalty is not None:
            pipeline_kwargs["gap_penalty"] = gap_penalty

        # Show progress
        if verbose:
            console.print(f"[bold blue]Source EPUB:[/bold blue] {source_epub}")
            console.print(f"[bold blue]Target EPUB:[/bold blue] {target_epub}")
            console.print(f"[bold blue]Language Pair:[/bold blue] {language_pair}")
            console.print(f"[bold blue]Method:[/bold blue] {method}")
            console.print(f"[bold blue]Format:[/bold blue] {format}")
            if pipeline_kwargs:
                console.print(f"[bold blue]Parameters:[/bold blue] {pipeline_kwargs}")

        # Create pipeline
        with console.status("[bold green]Creating pipeline..."):
            pipeline = VivrePipeline(language_pair, **pipeline_kwargs)

        # Process parallel EPUBs
        with console.status("[bold green]Processing EPUBs..."):
            alignments = pipeline.process_parallel_epubs(source_epub, target_epub)

        # Get book metadata for output
        source_parser = VivreParser()
        target_parser = VivreParser()

        source_title = getattr(source_parser, "_book_title", "Unknown")
        target_title = getattr(target_parser, "_book_title", "Unknown")
        book_title = source_title or target_title

        # Prepare output data
        output_data: dict = {
            "book_title": book_title,
            "language_pair": language_pair,
            "method": method,
            "source_epub": str(source_epub),
            "target_epub": str(target_epub),
            "total_alignments": len(alignments),
            "alignments": [],
        }

        # Add alignment details
        for i, (source_text, target_text) in enumerate(alignments, 1):
            alignment_data = {
                "id": i,
                "source": source_text,
                "target": target_text,
                "source_length": len(source_text),
                "target_length": len(target_text),
            }
            output_data["alignments"].append(alignment_data)

        # Format output based on requested format
        result: Union[str, dict]
        if format.lower() == "json":
            result = json.dumps(output_data, indent=2, ensure_ascii=False)
        elif format.lower() == "dict":
            result = output_data
        elif format.lower() == "text":
            result = _format_alignments_as_text(output_data)
        elif format.lower() == "csv":
            result = _format_alignments_as_csv(output_data)
        elif format.lower() == "xml":
            result = _format_alignments_as_xml(output_data)
        else:
            result = json.dumps(output_data, indent=2, ensure_ascii=False)

        # Output the result
        if output:
            if isinstance(result, dict):
                # For dict format, convert to JSON
                output_text = json.dumps(result, indent=2, ensure_ascii=False)
            else:
                # For other formats, result is already a string
                output_text = result

            output.write_text(output_text, encoding="utf-8")
            console.print(f"[green]✓[/green] Output written to [bold]{output}[/bold]")
        else:
            if verbose:
                # Show rich formatted summary
                console.print(
                    Panel(
                        f"[bold blue]Book Title:[/bold blue] {book_title}\n"
                        f"[bold blue]Language Pair:[/bold blue] {language_pair}\n"
                        f"[bold blue]Method:[/bold blue] {method}\n"
                        f"[bold blue]Total Alignments:[/bold blue] {len(alignments)}",
                        title="[bold green]Alignment Summary[/bold green]",
                        border_style="blue",
                    )
                )

                # Show alignment statistics
                if alignments:
                    source_lang, target_lang = language_pair.split("-")
                    table = Table(title="Alignment Statistics")
                    table.add_column("Metric", style="cyan")
                    table.add_column("Value", style="magenta")

                    # Calculate statistics
                    source_lengths = [len(src) for src, _ in alignments]
                    target_lengths = [len(tgt) for _, tgt in alignments]

                    table.add_row("Total Alignments", str(len(alignments)))
                    table.add_row(
                        "Avg Source Length",
                        f"{sum(source_lengths)/len(source_lengths):.1f}",
                    )
                    table.add_row(
                        "Avg Target Length",
                        f"{sum(target_lengths)/len(target_lengths):.1f}",
                    )
                    table.add_row("Max Source Length", str(max(source_lengths)))
                    table.add_row("Max Target Length", str(max(target_lengths)))

                    console.print(table)

                    # Show sample alignments
                    if len(alignments) > 0:
                        sample_table = Table(title="Sample Alignments (first 5)")
                        sample_table.add_column("#", style="cyan", justify="right")
                        sample_table.add_column(
                            f"{source_lang.upper()}", style="yellow"
                        )
                        sample_table.add_column(f"{target_lang.upper()}", style="green")

                        for i, (source_text, target_text) in enumerate(
                            alignments[:5], 1
                        ):
                            # Truncate for display
                            src_display = (
                                source_text[:50] + "..."
                                if len(source_text) > 50
                                else source_text
                            )
                            tgt_display = (
                                target_text[:50] + "..."
                                if len(target_text) > 50
                                else target_text
                            )
                            sample_table.add_row(str(i), src_display, tgt_display)

                        console.print(sample_table)

                        if len(alignments) > 5:
                            console.print(
                                f"[yellow]Note:[/yellow] Showing first 5 of {len(alignments)} alignments"
                            )
            else:
                # Show raw output
                if isinstance(result, dict):
                    console.print(JSON(json.dumps(result, ensure_ascii=False)))
                else:
                    console.print(result)

    except Exception as e:
        console.print(f"[red]Error aligning files:[/red] {e}")
        raise typer.Exit(1)


def _format_alignments_as_text(output_data: dict) -> str:
    """Format alignments as plain text."""
    lines = []
    lines.append(f"Book: {output_data['book_title']}")
    lines.append(f"Language Pair: {output_data['language_pair']}")
    lines.append(f"Method: {output_data['method']}")
    lines.append(f"Total Alignments: {output_data['total_alignments']}")
    lines.append("=" * 50)

    source_lang, target_lang = output_data["language_pair"].split("-")

    for alignment in output_data["alignments"]:
        lines.append(
            f"\n{alignment['id']}. {source_lang.upper()}: {alignment['source']}"
        )
        lines.append(f"   {target_lang.upper()}: {alignment['target']}")

    return "\n".join(lines)


def _format_alignments_as_csv(output_data: dict) -> str:
    """Format alignments as CSV with enhanced metadata."""
    source_lang, target_lang = output_data["language_pair"].split("-")

    # Enhanced CSV with metadata
    metadata_line = (
        f'"{output_data["book_title"]}","{output_data["language_pair"]}","{output_data["method"]}","{output_data["source_epub"]}","{output_data["target_epub"]}","{output_data["total_alignments"]}"'
    )
    lines = [
        "book_title,language_pair,method,source_epub,target_epub,total_alignments",
        metadata_line,
        "",  # Empty line to separate metadata from alignments
        f"id,{source_lang},{target_lang},source_length,target_length",
    ]

    for alignment in output_data["alignments"]:
        source_text = alignment["source"].replace('"', '""')  # Escape quotes
        target_text = alignment["target"].replace('"', '""')  # Escape quotes
        alignment_line = (
            f'"{alignment["id"]}","{source_text}","{target_text}","{alignment["source_length"]}","{alignment["target_length"]}"'
        )
        lines.append(alignment_line)

    return "\n".join(lines)


def _format_alignments_as_xml(output_data: dict) -> str:
    """Format alignments as XML."""
    source_lang, target_lang = output_data["language_pair"].split("-")

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<alignments>",
        f'  <book_title>{output_data["book_title"]}</book_title>',
        f'  <language_pair>{output_data["language_pair"]}</language_pair>',
        f'  <method>{output_data["method"]}</method>',
        f'  <source_epub>{output_data["source_epub"]}</source_epub>',
        f'  <target_epub>{output_data["target_epub"]}</target_epub>',
        f'  <total_alignments>{output_data["total_alignments"]}</total_alignments>',
    ]

    for alignment in output_data["alignments"]:
        xml_lines.extend(
            [
                f'  <alignment id="{alignment["id"]}">',
                f'    <source>{alignment["source"]}</source>',
                f'    <target>{alignment["target"]}</target>',
                f'    <source_length>{alignment["source_length"]}</source_length>',
                f'    <target_length>{alignment["target_length"]}</target_length>',
                "</alignment>",
            ]
        )

    xml_lines.append("</alignments>")

    return "\n".join(xml_lines)


@app.command()
def parse(
    epub_path: Path = typer.Argument(
        ...,
        help="Path to the EPUB file to parse",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    show_content: bool = typer.Option(
        False,
        "--show-content",
        "-c",
        help="Show chapter content (can be very long)",
    ),
    max_chapters: Optional[int] = typer.Option(
        None,
        "--max-chapters",
        "-m",
        help="Maximum number of chapters to display",
    ),
    format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format (json, dict, text, csv, xml)",
        case_sensitive=False,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: stdout)",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """
    Parse an EPUB file using the VivreParser.

    This command directly uses the parser to extract chapters and metadata
    from an EPUB file, providing detailed information about the structure.

    Examples:
        vivre parse book.epub
        vivre parse book.epub --show-content
        vivre parse book.epub --max-chapters 5
        vivre parse book.epub --output parsed.json
        vivre parse book.epub --format csv --output parsed.csv
    """
    try:
        # Validate format
        if format.lower() not in ["json", "dict", "text", "csv", "xml"]:
            console.print(
                f"[red]Invalid format:[/red] {format}. "
                f"Use 'json', 'dict', 'text', 'csv', or 'xml'"
            )
            raise typer.Exit(1)

        with console.status("[bold green]Parsing EPUB file..."):
            parser = VivreParser()
            chapters = parser.parse_epub(epub_path)

        # Get book metadata
        book_title = getattr(parser, "_book_title", "Unknown")
        book_author = getattr(parser, "_book_author", "Unknown")
        book_language = getattr(parser, "_book_language", "Unknown")

        # Prepare output data
        output_data: dict = {
            "file_path": str(epub_path),
            "book_title": book_title,
            "book_author": book_author,
            "book_language": book_language,
            "chapter_count": len(chapters),
            "chapters": [],
        }

        # Process chapters
        chapters_to_show = chapters
        if max_chapters is not None:
            chapters_to_show = chapters[:max_chapters]

        for i, (title, content) in enumerate(chapters_to_show, 1):
            chapter_data: dict = {
                "number": i,
                "title": title,
                "content_length": len(content),
                "word_count": len(content.split()),
                "character_count": len(content),
            }

            if show_content:
                chapter_data["content"] = content
            else:
                # Show preview
                preview = content[:200].strip()
                if len(content) > 200:
                    preview += "..."
                chapter_data["content_preview"] = preview

            output_data["chapters"].append(chapter_data)

        # Format output based on requested format
        result: Union[str, dict]
        if format.lower() == "json":
            result = json.dumps(output_data, indent=2, ensure_ascii=False)
        elif format.lower() == "dict":
            result = output_data
        elif format.lower() == "text":
            result = _format_parse_as_text(output_data)
        elif format.lower() == "csv":
            result = _format_parse_as_csv(output_data)
        elif format.lower() == "xml":
            result = _format_parse_as_xml(output_data)
        else:
            result = json.dumps(output_data, indent=2, ensure_ascii=False)

        # Output the result
        if output:
            if isinstance(result, dict):
                # For dict format, convert to JSON
                output_text = json.dumps(result, indent=2, ensure_ascii=False)
            else:
                # For other formats, result is already a string
                output_text = result

            output.write_text(output_text, encoding="utf-8")
            console.print(f"[green]✓[/green] Output written to [bold]{output}[/bold]")
        else:
            # Display with Rich formatting (only for interactive display)
            # Book information panel
            book_info = Panel(
                f"[bold blue]Title:[/bold blue] {book_title}\n"
                f"[bold blue]Author:[/bold blue] {book_author}\n"
                f"[bold blue]Language:[/bold blue] {book_language}\n"
                f"[bold blue]Chapters:[/bold blue] {len(chapters)}",
                title="[bold green]Book Information[/bold green]",
                border_style="blue",
            )
            console.print(book_info)

            # Chapters table
            if chapters_to_show:
                table = Table(title=f"Chapters ({len(chapters_to_show)} shown)")
                table.add_column("#", style="cyan", justify="right")
                table.add_column("Title", style="magenta")
                table.add_column("Words", style="yellow", justify="right")
                table.add_column("Characters", style="green", justify="right")

                if show_content:
                    table.add_column("Content", style="white", max_width=60)
                else:
                    table.add_column("Preview", style="white", max_width=60)

                for chapter in output_data["chapters"]:
                    if show_content:
                        # Truncate content for table display
                        content = chapter["content"]
                        if len(content) > 200:
                            content = content[:200] + "..."
                        table.add_row(
                            str(chapter["number"]),
                            chapter["title"],
                            str(chapter["word_count"]),
                            str(chapter["character_count"]),
                            content,
                        )
                    else:
                        table.add_row(
                            str(chapter["number"]),
                            chapter["title"],
                            str(chapter["word_count"]),
                            str(chapter["character_count"]),
                            chapter["content_preview"],
                        )

                console.print(table)

                if max_chapters and len(chapters) > max_chapters:
                    remaining = len(chapters) - max_chapters
                    console.print(
                        f"[yellow]Note:[/yellow] {remaining} more chapters not shown"
                    )

            # File information
            file_info = Panel(
                f"[bold blue]File:[/bold blue] {epub_path}\n"
                f"[bold blue]Size:[/bold blue] {epub_path.stat().st_size:,} bytes",
                title="[bold green]File Information[/bold green]",
                border_style="green",
            )
            console.print(file_info)

    except Exception as e:
        console.print(f"[red]Error parsing EPUB file:[/red] {e}")
        raise typer.Exit(1)


def _format_parse_as_text(output_data: dict) -> str:
    """Format parse results as plain text."""
    lines = []
    lines.append(f"File: {output_data['file_path']}")
    lines.append(f"Book Title: {output_data['book_title']}")
    lines.append(f"Author: {output_data['book_author']}")
    lines.append(f"Language: {output_data['book_language']}")
    lines.append(f"Chapters: {output_data['chapter_count']}")
    lines.append("=" * 50)

    for chapter in output_data["chapters"]:
        lines.append(f"\nChapter {chapter['number']}: {chapter['title']}")
        lines.append(f"Words: {chapter['word_count']}")
        lines.append(f"Characters: {chapter['character_count']}")
        if "content_preview" in chapter:
            lines.append(f"Preview: {chapter['content_preview']}")
        elif "content" in chapter:
            lines.append(f"Content: {chapter['content']}")

    return "\n".join(lines)


def _format_parse_as_csv(output_data: dict) -> str:
    """Format parse results as CSV."""
    lines = [
        "file_path,book_title,book_author,book_language,chapter_count",
        f'"{output_data["file_path"]}","{output_data["book_title"]}","{output_data["book_author"]}","{output_data["book_language"]}","{output_data["chapter_count"]}"',
        "",  # Empty line to separate metadata from chapters
        "chapter_number,title,word_count,character_count,content_preview",
    ]

    for chapter in output_data["chapters"]:
        title = chapter["title"].replace('"', '""')  # Escape quotes
        preview = chapter.get("content_preview", "").replace('"', '""')
        lines.append(
            f'"{chapter["number"]}","{title}","{chapter["word_count"]}","{chapter["character_count"]}","{preview}"'
        )

    return "\n".join(lines)


def _format_parse_as_xml(output_data: dict) -> str:
    """Format parse results as XML."""
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<epub_parse>",
        f'  <file_path>{output_data["file_path"]}</file_path>',
        f'  <book_title>{output_data["book_title"]}</book_title>',
        f'  <book_author>{output_data["book_author"]}</book_author>',
        f'  <book_language>{output_data["book_language"]}</book_language>',
        f'  <chapter_count>{output_data["chapter_count"]}</chapter_count>',
        "  <chapters>",
    ]

    for chapter in output_data["chapters"]:
        xml_lines.extend(
            [
                f'    <chapter number="{chapter["number"]}">',
                f'      <title>{chapter["title"]}</title>',
                f'      <word_count>{chapter["word_count"]}</word_count>',
                f'      <character_count>{chapter["character_count"]}</character_count>',
            ]
        )

        if "content_preview" in chapter:
            xml_lines.append(
                f'      <content_preview>{chapter["content_preview"]}</content_preview>'
            )
        elif "content" in chapter:
            xml_lines.append(f'      <content>{chapter["content"]}</content>')

        xml_lines.append("    </chapter>")

    xml_lines.extend(["  </chapters>", "</epub_parse>"])

    return "\n".join(xml_lines)


@app.command()
def read_epub(
    epub_path: Path = typer.Argument(
        ...,
        help="Path to the EPUB file to read",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    segment: bool = typer.Option(
        False,
        "--segment",
        "-s",
        help="Segment chapters into sentences",
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Language code for segmentation (auto-detected if not specified)",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: stdout)",
        file_okay=True,
        dir_okay=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output",
    ),
) -> None:
    """
    Read and parse an EPUB file.

    This command extracts chapters from an EPUB file and optionally segments
    them into sentences for further processing.

    Examples:
        vivre read book.epub
        vivre read book.epub --segment --language en
        vivre read book.epub --output chapters.json
    """
    try:
        with console.status("[bold green]Reading EPUB file..."):
            chapters = read(epub_path)

        # Prepare output data
        output_data: dict = {
            "book_title": chapters.book_title,
            "chapter_count": len(chapters.chapters),
            "chapters": [],
        }

        if segment:
            with console.status("[bold green]Segmenting chapters..."):
                chapters.segment(language=language)
                segmented = chapters.get_segmented()

                for title, sentences in segmented:
                    output_data["chapters"].append(
                        {
                            "title": title,
                            "sentence_count": len(sentences),
                            "sentences": sentences,
                        }
                    )
        else:
            # Just show chapter info
            for title, content in chapters.chapters:
                output_data["chapters"].append(
                    {
                        "title": title,
                        "content_length": len(content),
                        "content_preview": (
                            content[:100] + "..." if len(content) > 100 else content
                        ),
                    }
                )

        # Output the result
        output_json = json.dumps(output_data, indent=2, ensure_ascii=False)

        if output:
            output.write_text(output_json, encoding="utf-8")
            console.print(f"[green]✓[/green] Output written to [bold]{output}[/bold]")
        else:
            if verbose:
                # Show rich formatted output
                console.print(
                    Panel(
                        f"[bold blue]Book Title:[/bold blue] "
                        f"{output_data['book_title']}\n"
                        f"[bold blue]Chapters:[/bold blue] "
                        f"{output_data['chapter_count']}",
                        title="[bold green]EPUB Summary[/bold green]",
                    )
                )

                if output_data["chapters"]:
                    table = Table(title="Chapters")
                    table.add_column("Title", style="cyan")
                    table.add_column("Length", style="magenta")
                    table.add_column("Preview", style="yellow")

                    for chapter in output_data["chapters"]:
                        table.add_row(
                            chapter["title"],
                            str(
                                chapter.get(
                                    "content_length",
                                    chapter.get("sentence_count", "N/A"),
                                )
                            ),
                            chapter.get("content_preview", "N/A"),
                        )

                    console.print(table)
            else:
                # Show JSON output
                console.print(JSON(output_json))

    except Exception as e:
        console.print(f"[red]Error reading EPUB file:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def align_texts(
    source_epub: Path = typer.Argument(
        ...,
        help="Path to source language EPUB file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    target_epub: Path = typer.Argument(
        ...,
        help="Path to target language EPUB file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    languages: Optional[str] = typer.Option(
        None,
        "--languages",
        "--language-pair",
        "-l",
        help="Language pair code (e.g., 'en-es', auto-detected if not specified)",
    ),
    format: str = typer.Option(
        "json",
        "--format",
        "--form",
        "-f",
        help="Output format",
        case_sensitive=False,
    ),
    method: str = typer.Option(
        "gale-church",
        "--method",
        "-m",
        help="Alignment method",
        case_sensitive=False,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: stdout)",
        file_okay=True,
        dir_okay=False,
    ),
    c: Optional[float] = typer.Option(
        None,
        "--c",
        help="Gale-Church alignment parameter c",
    ),
    s2: Optional[float] = typer.Option(
        None,
        "--s2",
        help="Gale-Church alignment parameter s2",
    ),
    gap_penalty: Optional[float] = typer.Option(
        None,
        "--gap-penalty",
        help="Gale-Church gap penalty parameter",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed progress",
    ),
) -> None:
    """
    Align parallel EPUB files.

    This command aligns sentences between two parallel texts using the
    Gale-Church algorithm and outputs the results in various formats.

    Examples:
        vivre align english.epub spanish.epub
        vivre align book1.epub book2.epub --languages en-fr --format csv
        vivre align book1.epub book2.epub --c 1.1 --s2 7.0 --gap-penalty 2.5
    """
    try:
        # Validate format
        if format.lower() not in ["json", "dict", "text", "csv", "xml"]:
            console.print(
                f"[red]Invalid format:[/red] {format}. "
                f"Use 'json', 'dict', 'text', 'csv', or 'xml'"
            )
            raise typer.Exit(1)

        # Prepare alignment parameters
        align_kwargs: dict = {
            "method": method,
            "form": format.lower(),
        }

        if languages:
            align_kwargs["language_pair"] = languages

        # Add Gale-Church parameters if specified
        if c is not None:
            align_kwargs["c"] = c
        if s2 is not None:
            align_kwargs["s2"] = s2
        if gap_penalty is not None:
            align_kwargs["gap_penalty"] = gap_penalty

        # Show progress
        if verbose:
            console.print(f"[bold blue]Source EPUB:[/bold blue] {source_epub}")
            console.print(f"[bold blue]Target EPUB:[/bold blue] {target_epub}")
            if languages:
                console.print(f"[bold blue]Language Pair:[/bold blue] {languages}")
            console.print(f"[bold blue]Method:[/bold blue] {method}")
            console.print(f"[bold blue]Format:[/bold blue] {format}")

        # Perform alignment
        with console.status("[bold green]Aligning texts..."):
            result = align_api(source_epub, target_epub, **align_kwargs)

        # Output the result
        if output:
            if isinstance(result, dict):
                # For dict format, convert to JSON
                output_text = json.dumps(result, indent=2, ensure_ascii=False)
            else:
                # For other formats, result is already a string
                output_text = result

            output.write_text(output_text, encoding="utf-8")
            console.print(f"[green]✓[/green] Output written to [bold]{output}[/bold]")
        else:
            if verbose and isinstance(result, dict):
                # Show rich formatted output for dict/JSON
                console.print(
                    Panel(
                        f"[bold blue]Book Title:[/bold blue] "
                        f"{result.get('book_title', 'N/A')}\n"
                        f"[bold blue]Language Pair:[/bold blue] "
                        f"{result.get('language_pair', 'N/A')}\n"
                        f"[bold blue]Chapters:[/bold blue] "
                        f"{len(result.get('chapters', {}))}",
                        title="[bold green]Alignment Summary[/bold green]",
                    )
                )

                if result.get("chapters"):
                    table = Table(title="Aligned Chapters")
                    table.add_column("Chapter", style="cyan")
                    table.add_column("Title", style="magenta")
                    table.add_column("Alignments", style="yellow")

                    for chapter_num, chapter_data in result["chapters"].items():
                        table.add_row(
                            chapter_num,
                            chapter_data.get("title", "N/A"),
                            str(len(chapter_data.get("alignments", []))),
                        )

                    console.print(table)
            else:
                # Show raw output
                if isinstance(result, dict):
                    console.print(JSON(json.dumps(result, ensure_ascii=False)))
                else:
                    console.print(result)

    except Exception as e:
        console.print(f"[red]Error aligning files:[/red] {e}")
        raise typer.Exit(1)


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-V",
        help="Show version and exit",
        callback=lambda v: typer.echo("vivre 0.1.0") if v else None,
    ),
) -> None:
    """
    Vivre - A library for processing parallel texts.

    This CLI provides tools for reading EPUB files and aligning parallel texts
    using machine learning and corpus linguistics techniques.
    """
    pass


if __name__ == "__main__":
    app()
