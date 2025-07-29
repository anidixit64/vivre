#!/usr/bin/env python3
"""
Demonstration of dependency injection and pipeline caching in vivre.

This script shows how to use the new _pipeline parameter to improve performance
by reusing pipeline instances instead of creating new ones for each alignment.
"""

import time
from pathlib import Path

from vivre import align, clear_pipeline_cache
from vivre.integration import VivrePipeline


def demo_pipeline_caching():
    """Demonstrate the performance benefits of pipeline caching."""
    print("=== Pipeline Caching Demo ===")

    # Use the test data
    source_epub = (
        Path(__file__).parent.parent
        / "tests"
        / "data"
        / "Vacation Under the Volcano - Mary Pope Osborne.epub"
    )
    target_epub = (
        Path(__file__).parent.parent
        / "tests"
        / "data"
        / "Vacaciones al pie de un volcán.epub"
    )

    if not source_epub.exists() or not target_epub.exists():
        print("Test data not found. Please run this from the project root.")
        return

    # Clear cache to start fresh
    clear_pipeline_cache()

    print("1. First alignment (creates new pipeline):")
    start_time = time.time()
    result1 = align(source_epub, target_epub, "en-es")
    time1 = time.time() - start_time
    print(f"   Time: {time1:.2f} seconds")
    print(f"   Chapters found: {len(result1.to_dict()['chapters'])}")

    print("\n2. Second alignment (reuses cached pipeline):")
    start_time = time.time()
    result2 = align(source_epub, target_epub, "en-es")
    time2 = time.time() - start_time
    print(f"   Time: {time2:.2f} seconds")
    print(f"   Chapters found: {len(result2.to_dict()['chapters'])}")

    print(f"\nPerformance improvement: {time1/time2:.1f}x faster")
    print(f"Time saved: {time1 - time2:.2f} seconds")


def demo_dependency_injection():
    """Demonstrate dependency injection with custom pipeline."""
    print("\n=== Dependency Injection Demo ===")

    # Use the test data
    source_epub = (
        Path(__file__).parent.parent
        / "tests"
        / "data"
        / "Vacation Under the Volcano - Mary Pope Osborne.epub"
    )
    target_epub = (
        Path(__file__).parent.parent
        / "tests"
        / "data"
        / "Vacaciones al pie de un volcán.epub"
    )

    if not source_epub.exists() or not target_epub.exists():
        print("Test data not found. Please run this from the project root.")
        return

    # Create a custom pipeline with specific parameters
    custom_pipeline = VivrePipeline("en-es", c=1.1, s2=7.0, gap_penalty=2.5)
    print(
        f"Created custom pipeline with parameters: "
        f"c={custom_pipeline.aligner.c}, s2={custom_pipeline.aligner.s2}"
    )

    print("\n1. Alignment with custom pipeline (dependency injection):")
    start_time = time.time()
    result = align(source_epub, target_epub, "en-es", _pipeline=custom_pipeline)
    time1 = time.time() - start_time
    print(f"   Time: {time1:.2f} seconds")
    print(f"   Chapters found: {len(result.to_dict()['chapters'])}")

    print("\n2. Same alignment without dependency injection (creates new pipeline):")
    start_time = time.time()
    result2 = align(source_epub, target_epub, "en-es")
    time2 = time.time() - start_time
    print(f"   Time: {time2:.2f} seconds")
    print(f"   Chapters found: {len(result2.to_dict()['chapters'])}")

    print(f"\nDependency injection benefit: {time2/time1:.1f}x faster")
    print(f"Time saved: {time2 - time1:.2f} seconds")


def demo_multiple_alignments():
    """Demonstrate multiple alignments with shared pipeline."""
    print("\n=== Multiple Alignments Demo ===")

    # Use the test data
    source_epub = (
        Path(__file__).parent.parent
        / "tests"
        / "data"
        / "Vacation Under the Volcano - Mary Pope Osborne.epub"
    )
    target_epub = (
        Path(__file__).parent.parent
        / "tests"
        / "data"
        / "Vacaciones al pie de un volcán.epub"
    )

    if not source_epub.exists() or not target_epub.exists():
        print("Test data not found. Please run this from the project root.")
        return

    # Create a shared pipeline
    shared_pipeline = VivrePipeline("en-es")
    print("Created shared pipeline for multiple alignments")

    # Perform multiple alignments with the same pipeline
    results = []
    total_time = 0

    for i in range(3):
        print(f"\nAlignment {i+1}:")
        start_time = time.time()
        result = align(source_epub, target_epub, "en-es", _pipeline=shared_pipeline)
        alignment_time = time.time() - start_time
        total_time += alignment_time
        results.append(result)

        print(f"   Time: {alignment_time:.2f} seconds")
        print(f"   Chapters: {len(result.to_dict()['chapters'])}")

    print(
        f"\nTotal time for 3 alignments with shared pipeline: {total_time:.2f} seconds"
    )
    print(f"Average time per alignment: {total_time/3:.2f} seconds")


if __name__ == "__main__":
    print("Vivre Dependency Injection and Pipeline Caching Demo")
    print("=" * 50)

    try:
        demo_pipeline_caching()
        demo_dependency_injection()
        demo_multiple_alignments()

        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("\nKey benefits:")
        print("- Pipeline caching reduces initialization overhead")
        print("- Dependency injection allows custom pipeline reuse")
        print("- Multiple alignments benefit from shared resources")

    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure you're running this from the project root directory.")
