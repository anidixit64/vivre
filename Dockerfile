# Dockerfile for vivre project
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/
COPY tests/ ./tests/

# Set Python path
ENV PYTHONPATH=/app/src

# Default command
CMD ["python", "-m", "vivre"]
