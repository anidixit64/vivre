"""
Command-line interface for the vivre library.

This module provides a CLI for common tasks like reading EPUB files
and aligning parallel texts.
"""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from .api import align, read
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
    """
    try:
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

        # Output the result
        if output:
            # Write to file
            output_json = json.dumps(output_data, indent=2, ensure_ascii=False)
            output.write_text(output_json, encoding="utf-8")
            console.print(f"[green]✓[/green] Output written to [bold]{output}[/bold]")
        else:
            # Display with Rich formatting
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
        if format.lower() not in ["json", "dict", "text", "csv"]:
            console.print(
                f"[red]Invalid format:[/red] {format}. "
                f"Use 'json', 'dict', 'text', or 'csv'"
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
            result = align(source_epub, target_epub, **align_kwargs)

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
