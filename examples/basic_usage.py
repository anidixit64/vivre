#!/usr/bin/env python3
"""
Basic usage examples for the vivre library.

This script demonstrates how to use the vivre library for common tasks.
"""

from pathlib import Path

# Import the vivre library
import vivre


def example_parse_epub():
    """Example: Parse an EPUB file and extract chapters."""
    print("=== Example: Parse EPUB ===")

    # Find a test EPUB file
    test_files = list(Path("tests/data").glob("*.epub"))
    if not test_files:
        print("No test EPUB files found in tests/data/")
        return

    epub_file = test_files[0]
    print(f"Parsing: {epub_file}")

    try:
        # Parse the EPUB file
        chapters = vivre.read(epub_file)
        print(f"Found {len(chapters)} chapters")
        print(f"Book title: {chapters.book_title}")

        # Show first chapter info
        if chapters:
            title, content = chapters[0]
            print(f"First chapter: {title}")
            print(f"Content length: {len(content)} characters")
            print(f"Word count: {len(content.split())} words")

        # Segment into sentences
        segmented = chapters.segment()
        sentences = segmented.get_segmented()
        print(f"Total sentences: {sum(len(s) for _, s in sentences)}")

    except Exception as e:
        print(f"Error: {e}")


def example_quick_align():
    """Example: Quick alignment of two EPUB files."""
    print("\n=== Example: Quick Alignment ===")

    # Find test EPUB files
    test_files = list(Path("tests/data").glob("*.epub"))
    if len(test_files) < 2:
        print("Need at least 2 test EPUB files for alignment")
        return

    source_file = test_files[0]
    target_file = test_files[1]
    print(f"Aligning: {source_file} ↔ {target_file}")

    try:
        # Quick alignment - returns simple sentence pairs
        pairs = vivre.quick_align(source_file, target_file)
        print(f"Found {len(pairs)} aligned sentence pairs")

        # Show first few pairs
        for i, (source, target) in enumerate(pairs[:3], 1):
            print(f"\nPair {i}:")
            print(f"  Source: {source[:100]}...")
            print(f"  Target: {target[:100]}...")

    except Exception as e:
        print(f"Error: {e}")


def example_full_align():
    """Example: Full alignment with metadata and formatting."""
    print("\n=== Example: Full Alignment ===")

    # Find test EPUB files
    test_files = list(Path("tests/data").glob("*.epub"))
    if len(test_files) < 2:
        print("Need at least 2 test EPUB files for alignment")
        return

    source_file = test_files[0]
    target_file = test_files[1]
    print(f"Aligning: {source_file} ↔ {target_file}")

    try:
        # Full alignment with JSON output
        result = vivre.align(source_file, target_file, form="json")
        print("JSON output (first 500 chars):")
        print(result[:500] + "..." if len(result) > 500 else result)

        # Get as dictionary for programmatic access
        data = vivre.align(source_file, target_file, form="dict")
        print("\nMetadata:")
        print(f"  Book title: {data['book_title']}")
        print(f"  Language pair: {data['language_pair']}")
        print(f"  Total alignments: {data['total_alignments']}")

        # Show text format
        text_result = vivre.align(source_file, target_file, form="text")
        print("\nText output (first 300 chars):")
        print(text_result[:300] + "..." if len(text_result) > 300 else text_result)

    except Exception as e:
        print(f"Error: {e}")


def example_supported_languages():
    """Example: Check supported languages."""
    print("\n=== Example: Supported Languages ===")

    try:
        languages = vivre.get_supported_languages()
        print(f"Supported languages: {', '.join(languages)}")
        print(f"Total: {len(languages)} languages")

    except Exception as e:
        print(f"Error: {e}")


def example_advanced_usage():
    """Example: Advanced usage with classes."""
    print("\n=== Example: Advanced Usage ===")

    # Find test EPUB files
    test_files = list(Path("tests/data").glob("*.epub"))
    if len(test_files) < 2:
        print("Need at least 2 test EPUB files for advanced example")
        return

    source_file = test_files[0]
    target_file = test_files[1]

    try:
        # Use the pipeline directly
        from vivre import VivrePipeline

        # Create pipeline with custom parameters
        pipeline = VivrePipeline("en-es", c=1.1, s2=7.0)

        # Process the files
        alignments = pipeline.process_parallel_epubs(source_file, target_file)

        print(f"Pipeline processed {len(alignments)} alignments")

        # Show pipeline info
        info = pipeline.get_pipeline_info()
        print(f"Pipeline info: {info}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples."""
    print("Vivre Library - Basic Usage Examples")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("tests/data").exists():
        print("Please run this script from the project root directory")
        print("(where tests/data/ exists)")
        return

    # Run examples
    example_parse_epub()
    example_quick_align()
    example_full_align()
    example_supported_languages()
    example_advanced_usage()

    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nFor more information:")
    print("  - API docs: help(vivre)")
    print("  - CLI help: vivre --help")
    print("  - README: https://github.com/your-repo/vivre")


if __name__ == "__main__":
    main()
