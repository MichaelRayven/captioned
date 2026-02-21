# Variables
compose_file := "infra/docker/docker-compose.local.yaml"
project_dir := "."

default:
    @just --list

# --- Docker Commands ---

[group('docker')]
up:
    docker compose -f {{compose_file}} --project-directory {{project_dir}} up -d

[group('docker')]
down:
    docker compose -f {{compose_file}} --project-directory {{project_dir}} down

[group('docker')]
build:
    docker compose -f {{compose_file}} --project-directory {{project_dir}} build

[group('docker')]
logs *args:
    docker compose -f {{compose_file}} --project-directory {{project_dir}} logs -f {{args}}

[group('docker')]
ps:
    docker compose -f {{compose_file}} --project-directory {{project_dir}} ps

# --- Local Development (using uv) ---

[group('dev')]
install:
    uv sync --dev
    uv run prek install

[group('dev')]
run:
    uv run fastapi dev src/app/main.py --port 8000

[group('dev')]
worker:
    uv run celery -A src.app.worker.celery_app worker --loglevel=info

# --- Database & Migrations ---

[group('db')]
migrate:
    uv run alembic upgrade head

[group('db')]
makemigrations message:
    uv run alembic revision --autogenerate -m "{{message}}"

# --- Quality ---

[group('lint')]
lint:
    uv run ruff check .
    uv run ruff format --check .

[group('lint')]
format:
    uv run ruff format .
