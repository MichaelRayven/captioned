# Variables
docker_dir := "infra/docker"
project_dir := "."

default:
    @just --list

# --- Docker Commands ---

[group('docker')]
up config:
    docker compose -f "{{docker_dir}}/docker-compose.{{config}}.yaml" --project-directory {{project_dir}} up -d

[group('docker')]
down config:
    docker compose -f "{{docker_dir}}/docker-compose.{{config}}.yaml" --project-directory {{project_dir}} down

[group('docker')]
build config:
    docker compose -f "{{docker_dir}}/docker-compose.{{config}}.yaml" --project-directory {{project_dir}} build

[group('docker')]
logs config *args:
    docker compose -f "{{docker_dir}}/docker-compose.{{config}}.yaml" --project-directory {{project_dir}} logs {{args}}

[group('docker')]
ps config:
    docker compose -f "{{docker_dir}}/docker-compose.{{config}}.yaml" --project-directory {{project_dir}} ps

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

[group('migrations')]
migrate:
    uv run alembic upgrade head

[group('migrations')]
makemigrations message:
    uv run alembic revision --autogenerate -m "{{message}}"

# --- Quality ---

[group('quality')]
lint:
    uv run ruff check .
    uv run ruff format --check .

[group('quality')]
format:
    uv run ruff format .

[group('quality')]
test:
    uv run pytest

[group('quality')]
coverage:
    uv run pytest --cov=src/app
