.PHONY: help install install-dev test test-cov lint format type-check clean build docs serve-docs docker-build docker-test docker-shell

# Default target
help:
	@echo "Vivre Development Commands"
	@echo "========================"
	@echo ""
	@echo "Installation:"
	@echo "  install      - Install the package in development mode"
	@echo "  install-dev  - Install with development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test         - Run all tests"
	@echo "  test-cov     - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with ruff"
	@echo "  type-check   - Run type checking with mypy"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         - Build documentation"
	@echo "  serve-docs   - Serve documentation locally"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-test  - Run tests in Docker"
	@echo "  docker-shell - Start interactive Docker shell"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        - Clean up cache and build files"
	@echo "  build        - Build distribution packages"

# Installation
install:
	pip install -e .

install-dev: install
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src/vivre --cov-report=html --cov-report=term-missing

# Code Quality
lint:
	ruff check .

format:
	ruff format .

type-check:
	mypy src/ tests/

# Documentation
docs:
	cd docs && make html

serve-docs: docs
	cd docs/_build/html && python -m http.server 8000

# Docker
docker-build:
	docker build -t vivre .

docker-test: docker-build
	docker run --rm vivre python -m pytest tests/ -v

docker-shell: docker-build
	docker run --rm -it vivre /bin/bash

# Maintenance
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".coverage" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".mypy_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".ruff_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/ htmlcov/

build: clean
	python -m build

# Development workflow
dev-setup: install-dev
	@echo "Installing spaCy models..."
	python -m spacy download en_core_web_sm
	python -m spacy download es_core_news_sm
	python -m spacy download fr_core_news_sm
	python -m spacy download it_core_news_sm
	@echo "Development setup complete!"

pre-commit-all:
	pre-commit run --all-files

# Quick checks
check: lint type-check test
	@echo "All checks passed!"

# Release preparation
release-prep: clean test-cov lint type-check
	@echo "Release preparation complete!"
