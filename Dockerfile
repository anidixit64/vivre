# Dockerfile for vivre project
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install poetry
RUN pip install poetry

# Install dependencies (excluding dev dependencies and root project)
RUN poetry install --no-root --no-dev

# Install the project itself
RUN poetry install --only-root

# Set Python path
ENV PYTHONPATH=/app/src

# Default command
CMD ["python", "-m", "vivre"]
