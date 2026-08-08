# CodeGuard AI Backend

FastAPI-based backend service for the CodeGuard AI platform. Provides REST API endpoints for GitHub PR analysis, AI agent orchestration, and review result management.

## Tech Stack

- **Python 3.11+**
- **FastAPI** — High-performance async web framework
- **Pydantic v2** — Data validation and settings management
- **SQLAlchemy 2.0** — Async ORM with SQLite (dev) / PostgreSQL (prod)
- **httpx** — Async HTTP client for GitHub API
- **pytest** — Testing framework with async support
- **ruff** — Fast Python linter

## Project Structure

```
backend/
├── app/
│   ├── api/           # REST API routes
│   ├── agents/        # AI agents (Bug, Security, Code Quality, Test)
│   ├── core/          # Configuration, database, security
│   ├── schemas/       # Pydantic models
│   ├── services/      # Business logic (GitHub, DiffParser, AIProvider)
│   └── skills/        # Custom PR review skill engine
├── tests/             # Unit and integration tests
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project metadata and tool config
└── .env.example       # Environment variable template
```

## Quick Start

### Prerequisites

- Python 3.11+
- Git

### Installation

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Required for full functionality:
# - GITHUB_TOKEN: GitHub Personal Access Token
# - AI_API_KEY: API key for AI provider (Gemini/NVIDIA)
# - DATABASE_URL: PostgreSQL connection string (optional, defaults to SQLite)
```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/review` | Submit a GitHub PR URL for analysis |
| `GET` | `/api/v1/review/{review_id}` | Get review results by ID |
| `GET` | `/api/v1/health` | Health check endpoint |

## Running Tests

```bash
# Run all tests with coverage
pytest -v --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

Target: **85% minimum test coverage**

## Linting & Formatting

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

## Environment Variables

See `.env.example` for all available options:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes* | — | GitHub PAT for API access |
| `AI_PROVIDER` | No | `mock` | AI provider: `gemini`, `nvidia`, `mock` |
| `AI_API_KEY` | Yes* | — | API key for selected AI provider |
| `DATABASE_URL` | No | SQLite | PostgreSQL connection string |
| `PORT` | No | `8000` | Server port |
| `HOST` | No | `0.0.0.0` | Server host |
| `ENVIRONMENT` | No | `development` | Environment mode |

*Required for non-mock AI provider and GitHub API access

## AI Provider Configuration

The backend supports multiple AI providers through the `AIProvider` abstraction:

- **Mock** (default): Deterministic offline responses for testing
- **Gemini**: Google's Generative AI (requires `AI_API_KEY`)
- **NVIDIA NIM**: NVIDIA's inference microservices (requires `AI_API_KEY`)

Set `AI_PROVIDER` and `AI_API_KEY` in `.env` to use a real AI provider.

## Database

- **Development**: SQLite (`sqlite+aiosqlite:///./codeguard.db`) — zero config
- **Production**: PostgreSQL (Neon, Supabase, etc.) — set `DATABASE_URL`

Run migrations (if using Alembic):
```bash
alembic upgrade head
```

## Project Architecture

See [System Architecture](../docs/architecture.md) and [Agent Constitution](../AGENTS.md) for detailed documentation.