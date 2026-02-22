# Captioned

> Intelligent tools for content creators.

Captioned is a modern web application for editing videos, automatically generating captions using AI, and converting media files. Built with a microservice architecture and powered by FFmpeg under the hood.

## ✨ Features

- 🎬 **Video Editing** - Trim, crop, and edit videos with ease
- 🤖 **AI-Powered Captions** - Automatic caption generation using AI
- 🔄 **Media Conversion** - Convert between various video and audio formats
- ⚡ **Async Processing** - Fast, non-blocking operations using async/await
- 📦 **Microservice Architecture** - Scalable and maintainable service design
- 🚀 **Task Queue** - Background job processing with Celery and RabbitMQ

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (async) - Database toolkit
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Relational database
- **Cache**: [Redis](https://redis.io/) - In-memory data store
- **Message Queue**: [RabbitMQ](https://www.rabbitmq.com/) - Message broker
- **Task Queue**: [Celery](https://docs.celeryq.dev/) - Distributed task queue
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- **Testing**: [pytest](https://pytest.org/) - Testing framework
- **Linting**: [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter

## 📋 Prerequisites

- Python 3.14+
- [Docker](https://www.docker.com/) & Docker Compose
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [just](https://github.com/casey/just) - Command runner
- FFmpeg (for video processing)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/captioned.git
cd captioned
```

### 2. Install dependencies

```bash
just install
```

### 3. Start infrastructure services

```bash
just up infra
```

This starts PostgreSQL, Redis, and RabbitMQ using Docker Compose.

### 4. Run database migrations

```bash
just migrate
```

### 5. Start the development server

```bash
# Terminal 1 - API Server
just run

# Terminal 2 - Celery Worker
just worker
```

The API will be available at `http://localhost:8000`

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`

## 📁 Project Structure

```
captioned/
├── infra/
│   └── docker/
│       └── docker-compose.local.yaml
│       └── docker-compose.infra.yaml
├── src/
│   └── app/
│       ├── api/              # API routes and endpoints
│       ├── core/             # Core configuration
│       ├── models/           # SQLAlchemy models
│       ├── schemas/          # Pydantic schemas
│       ├── services/         # Business logic
│       ├── worker/           # Celery tasks
│       └── main.py           # Application entry point
├── tests/                    # Test suite
├── alembic/                  # Database migrations
├── justfile                  # Command runner recipes
├── pyproject.toml           # Project dependencies
└── README.md
```

## 🎯 Available Commands

All commands are managed using [just](https://github.com/casey/just). Run `just` to see all available commands.

### Docker Commands

There are two docker-compose configurations available:
1. infra - Postgres, Redis, RabbitMQ, etc.
2. local - Extends infra with containers for FastAPI, Celery.

```bash
just up [config]              # Start all services
just down [config]            # Stop all services
just build [config]           # Build Docker images
just logs [config] [args]     # View logs
just ps [config]              # List running containers
```

### Development Commands

```bash
just install         # Install dependencies
just run             # Run FastAPI dev server
just worker          # Run Celery worker
```

### Database Commands

```bash
just migrate                    # Run pending migrations
just makemigrations "message"   # Create new migration
```

### Quality Commands

```bash
just lint            # Run linting checks
just format          # Format code
just test            # Run tests
just coverage        # Run tests with coverage
```

## 🧪 Testing

```bash
# Run all tests
just test

# Run with coverage report
just coverage

# Run specific test file
uv run pytest tests/test_specific.py

# Run with verbose output
uv run pytest -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
