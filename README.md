# 🛡️ CodeGuard AI

> **AI-Powered Pull Request Review & Developer Productivity Platform**  
> *Track B: Developer Productivity Tools — Deploy or Die: HowToAlgo x GDG on Campus KIIT Hackathon*

CodeGuard AI is an automated PR analysis platform built for real developer workflows. It ingests GitHub Pull Requests, extracts unified diff patches, executes specialized domain AI agents (Bugs, Security, Code Quality, Test Coverage), deduplicates findings, and presents a developer-focused actionable review dashboard.

---

## 🌟 Key Features

- **GitHub Integration**: Fetch PR metadata, author details, changed files, and unified git diffs directly via GitHub REST API.
- **Specialized Multi-Agent Pipeline**:
  - 🐛 **Bug Detection Agent**: Runtime exceptions, off-by-one errors, null pointer dereferences, logic flaws.
  - 🔒 **Security Review Agent**: OWASP vulnerabilities, hardcoded secrets, injection vectors, unsafe inputs.
  - ⚡ **Code Quality Agent**: Code smells, duplication, cognitive complexity, bad abstractions.
  - 🧪 **Test Analysis Agent**: Missing test cases on new/modified code branches and runnable test snippets.
- **Custom PR Review Skill**: 10-step repeatable process engine parsing diffs and orchestrating agent execution.
- **AI Provider Abstraction**: Switch between Google Gemini, Nvidia NIM, and deterministic offline `MockAIProvider`.
- **Developer-Focused UI**: Dark-mode dashboard with interactive filtering by severity/category and one-click code fix copy.
- **Green CI/CD Pipeline**: GitHub Actions running backend linting, pytest suite, frontend build, vitest, and Playwright E2E tests.

---

## 🏗️ Architecture & Specs

Detailed documentation is available in the `docs/` folder:
- 📄 [System Architecture](docs/architecture.md)
- 📋 [Product Requirements Document (PRD)](docs/PRD.md)
- 🤖 [Agent Constitution & Rules](AGENTS.md)
- 🧠 [Custom Agents & Skills Spec](AGENTS_AND_SKILLS.md)

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git

### 1. Repository Setup

```bash
git clone https://github.com/your-org/codeguard-ai.git
cd codeguard-ai
```

### 2. Backend Setup

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

# Configure environment
cp .env.example .env
# Edit .env with your GitHub token, AI API key, and database URL
```

Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

Backend API: `http://localhost:8000` | Swagger Docs: `http://localhost:8000/docs`

> **Backend Environment Variables**: See [backend/.env.example](backend/.env.example) and [backend/README.md](backend/README.md)

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional - defaults to http://localhost:8000)
cp .env.example .env
```

Start the development server:
```bash
npm run dev
```

Frontend Dashboard: `http://localhost:5173`

> **Frontend Environment Variables**: See [frontend/.env.example](frontend/.env.example) and [frontend/README.md](frontend/README.md)

---

## 🧪 Running Tests

### Backend Unit & Integration Tests (Pytest)

```bash
cd backend
pytest -v --cov=app --cov-report=term-missing
```

### Frontend Build & Unit Verification

```bash
cd frontend
npm run build
npm run lint
```

### Playwright End-to-End Tests

```bash
cd frontend
npx playwright test
```

---

## 🎬 Demo Instructions (Hackathon Presentation)

1. Open `http://localhost:5173` in your browser.
2. Enter a GitHub Pull Request URL (or select sample PR from the quick loader). Example: `https://github.com/octocat/Hello-World/pull/1`.
3. Click **"Analyze Pull Request"**.
4. Observe the multi-agent pipeline progress indicators in real-time.
5. Review the **PR Health Score**, **Severity Breakdown Pills**, and **Interactive Findings**.
6. Filter findings by `SECURITY` or `BUG` categories.
7. Click on a finding to view file line location, rationale, and copy the suggested code fix.

---

## 📁 Project Structure

```
codeguard-ai/
├── backend/                 # FastAPI backend service
│   ├── app/                # Application code
│   ├── tests/              # Pytest test suite
│   ├── .env.example        # Backend environment template
│   ├── README.md           # Backend documentation
│   └── requirements.txt    # Python dependencies
├── frontend/               # React + TypeScript + Vite frontend
│   ├── src/                # Source code
│   ├── e2e/                # Playwright E2E tests
│   ├── .env.example        # Frontend environment template
│   ├── README.md           # Frontend documentation
│   └── package.json        # Node dependencies
├── docs/                   # Architecture & PRD documentation
├── .env.example            # Root environment template (references sub-projects)
├── AGENTS.md               # Agent constitution & rules
├── AGENTS_AND_SKILLS.md    # Custom agents & skills specification
└── README.md               # This file
```

---

## 🔐 Environment Configuration

Each sub-project has its own `.env.example` file:

| Project | Template | Required Variables |
|---------|----------|-------------------|
| **Backend** | `backend/.env.example` | `GITHUB_TOKEN`, `AI_API_KEY`, `DATABASE_URL` |
| **Frontend** | `frontend/.env.example` | `VITE_API_BASE_URL` (optional) |

**Never commit `.env` files** — they are in `.gitignore`. Copy `.env.example` to `.env` in each project directory and fill in your values.

---

## 📜 License

MIT License. Developed for the HowToAlgo x GDG on Campus KIIT Hackathon.