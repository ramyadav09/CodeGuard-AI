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

### 1. Repository Setup & Environment
```bash
git clone https://github.com/your-org/codeguard-ai.git
cd codeguard-ai

# Copy environment variables
cp .env.example .env
```

Edit `.env` to add your keys (optional for test mode):
```env
GITHUB_TOKEN=your_github_token
AI_PROVIDER=gemini # or 'mock' for local offline testing
AI_API_KEY=your_gemini_api_key
```

### 2. Backend Installation & Execution
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend API will be available at `http://localhost:8000`. API Swagger docs at `http://localhost:8000/docs`.

### 3. Frontend Installation & Execution
```bash
cd frontend
npm install
npm run dev
```
Web application dashboard will be live at `http://localhost:5173`.

---

## 🧪 Running Tests

### Backend Unit & Integration Tests (Pytest)
```bash
cd backend
pytest -v
```

### Frontend Build & Unit Verification
```bash
cd frontend
npm run build
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

## 📜 License

MIT License. Developed for the HowToAlgo x GDG on Campus KIIT Hackathon.
