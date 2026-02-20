# Install uv
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.14-slim AS runtime

RUN adduser --disabled-password --gecos '' appuser

# Copy the environment and source code
COPY --from=builder --chown=appuser:appuser /app /app

WORKDIR /app

# Activate Python virtual environment
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

# Run the application
CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
