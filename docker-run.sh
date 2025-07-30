#!/bin/bash

# Helper script for running the vivre Docker container

case "${1:-tests}" in
    "tests")
        echo "Running test suite..."
        docker run --rm vivre python -m pytest tests/ -v
        ;;
    "shell")
        echo "Starting interactive shell with vivre library ready..."
        docker run --rm -it vivre /bin/bash
        ;;
    "cli")
        echo "Running vivre CLI..."
        docker run --rm vivre python -m vivre --help
        ;;
    "help")
        echo "Usage: $0 [tests|shell|cli|help]"
        echo "  tests  - Run the test suite (default)"
        echo "  shell  - Drop into interactive shell"
        echo "  cli    - Show vivre CLI help"
        echo "  help   - Show this help message"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
