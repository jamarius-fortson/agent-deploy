DOCKERFILE_TEMPLATE = """
# Stage 1: Build
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

WORKDIR /app

# Install dependencies separately to leverage caching
COPY pyproject.toml .
RUN uv sync --no-dev

# Stage 2: Run
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy the virtualenv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy the source code
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV ADEPLOY_CONFIG=adeploy.yaml

EXPOSE 8000

CMD ["python", "-m", "agent_deploy.cli.main", "run", "--port", "8000", "--no-reload"]
"""

def generate_dockerfile() -> str:
    return DOCKERFILE_TEMPLATE.strip()
