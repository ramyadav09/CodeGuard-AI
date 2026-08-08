# Architecture Document — CodeGuard AI

## 1. Executive System Overview

**CodeGuard AI** is an enterprise-grade AI-powered developer productivity platform designed to automate GitHub Pull Request reviews. The system extracts PR metadata and unified diff patches via the GitHub REST API, processes code changes through a specialized multi-agent analysis pipeline, validates structured AI findings against strict Pydantic schemas, and presents actionable recommendations in a high-density web dashboard.

---

## 2. High-Level System Architecture

```
                               ┌────────────────────────────────┐
                               │       GitHub REST API v3       │
                               └───────────────┬────────────────┘
                                               │ PR Metadata & Diffs
                                               v
┌─────────────────────────┐       ┌─────────────────────────────┐
│  React 18 + Vite Web UI │  HTTP │     FastAPI Backend Core    │
│  (Tailwind + TypeScript)│<----->│  (Async Uvicorn + Pydantic) │
└─────────────────────────┘       └──────────────┬──────────────┘
                                                 │ Unified Diff Object
                                                 v
                                      ┌─────────────────────┐
                                      │   PR Review Skill   │
                                      └──────────┬──────────┘
                                                 │ Orchestration
               ┌───────────────────┬─────────────┼───────────────────┬───────────────────┐
               │                   │             │                   │                   │
               v                   v             v                   v                   v
      ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
      │  Bug Detection  │  │   Security   │  │ Code Quality │  │ Test Analysis│  │  Review      │
      │      Agent      │  │    Agent     │  │    Agent     │  │    Agent     │  │  Aggregator  │
      └────────┬────────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
               │                  │                 │                 │                 │
               └──────────────────┴─────────┬───────┴─────────────────┴─────────────────┘
                                            │ AI Provider Interface
                                            v
                               ┌──────────────────────────────┐
                               │  Gemini / Nvidia / Mock AI   │
                               └──────────────────────────────┘
```

---

## 3. Component Architecture & Data Flow

### 3.1 Data Flow Sequence
1. **User Request**: User inputs a GitHub repository and PR number (or full PR URL) in the Web UI.
2. **PR Fetching**: FastAPI backend calls `GitHubService` to fetch PR title, description, author, target branches, modified files, and raw diff patch data.
3. **Diff Parsing**: `DiffParser` breaks down raw git diffs into structured file changes, line numbers, added lines, and removed lines.
4. **Skill Engine Execution**: `PRReviewSkill` isolates code changes from noise (e.g. lockfiles, docs) and formats prompts for specialized agents.
5. **Multi-Agent Pipeline**:
   - `BugDetectionAgent` checks for runtime bugs, off-by-one errors, null pointers, logic gaps.
   - `SecurityReviewAgent` checks for credentials, injection points, unvalidated inputs, OWASP risks.
   - `CodeQualityAgent` checks for code duplication, high complexity, bad abstractions, dead code.
   - `TestAnalysisAgent` checks for missing test coverage on new/modified branches and generates test specifications.
6. **Provider Execution**: Agents query `AIProvider` (`GeminiProvider` in production, `MockAIProvider` in test/CI mode).
7. **Aggregation & Scoring**: `ReviewAggregator` deduplicates findings across agents, calculates an overall score (0-100), orders findings by severity (`CRITICAL` > `HIGH` > `MEDIUM` > `LOW` > `INFO`), and saves the result to SQLite/PostgreSQL.
8. **Dashboard Render**: Web UI renders interactive finding cards, file filter bar, severity breakdown, and actionable fix snippets.

---

## 4. Frontend Architecture (`frontend/`)

- **Framework**: React 18 with TypeScript compiled via Vite for instant HMR and optimized builds.
- **Styling**: Vanilla Tailwind CSS paired with custom CSS variables for dark-mode developer aesthetics (Inter and JetBrains Mono typography).
- **State Management**: React state hooks (`useState`, `useReducer`) for filter states (severity, category, file search) and API data fetching.
- **Component Breakdown**:
  - `Navbar`: Header banner with branding, active backend health indicator, and repository search bar.
  - `MetricsOverview`: Metric cards showing Overall PR Health Score, Total Findings Count, and Critical/High risk pills.
  - `PRInputForm`: Intuitive form supporting URL parsing and direct repo/PR inputs.
  - `FilterBar`: Toggle buttons for Severities (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`) and Categories (`BUG`, `SECURITY`, `CODE_QUALITY`, `TESTING`, `PERFORMANCE`).
  - `FindingCard`: Expandable card displaying Severity badge, Line locations, Problem description, Rationale, Confidence rating, and copyable Code Fix.

---

## 5. Backend Architecture (`backend/`)

- **Framework**: FastAPI (Python 3.11+) powered by Uvicorn.
- **Key Layers**:
  - `api/`: REST routing layer (`/api/v1/review`, `/api/v1/health`, `/api/v1/recent`).
  - `core/`: Environment settings, database connection manager, exception handling.
  - `models/`: SQLAlchemy ORM definitions (`Repository`, `PullRequest`, `ReviewReport`, `Finding`).
  - `schemas/`: Pydantic v2 schemas (`PRReviewRequest`, `FindingSchema`, `PRReviewResponse`).
  - `services/`: `GitHubService` (httpx client for GitHub API), `DiffParser` (patch analysis), `AIProvider` (LLM abstraction).
  - `agents/`: Domain agent implementations extending `BaseAgent`.
  - `skills/`: `PRReviewSkill` orchestration workflow engine.

---

## 6. AI Provider Abstraction Layer

To ensure vendor lock-in avoidance, the application relies on an abstract base class `AIProvider`:

```python
class AIProvider(ABC):
    @abstractmethod
    async def analyze_diff(self, prompt: str, schema: Type[BaseModel]) -> Dict[str, Any]:
        """Sends structured analysis prompt to the LLM and returns validated schema dictionary."""
        pass
```

### Implementations:
1. `GeminiProvider`: Uses Google Gemini API to analyze diffs with structured JSON output enforcement.
2. `NvidiaProvider`: Alternative LLM endpoint for Nvidia NIM / OpenAI compatible completions.
3. `MockAIProvider`: Zero-latency, deterministic provider returning pre-configured test fixtures. Used exclusively during unit and Playwright E2E tests.

---

## 7. Database Model (SQLAlchemy / SQLite & Neon PostgreSQL)

```
┌────────────────────────┐         ┌────────────────────────┐
│       Repository       │ 1     * │      PullRequest       │
├────────────────────────┤─────────├────────────────────────┤
│ id (PK)                │         │ id (PK)                │
│ owner (String)         │         │ repository_id (FK)     │
│ name (String)          │         │ pr_number (Integer)    │
│ url (String)           │         │ title (String)         │
└────────────────────────┘         │ author (String)        │
                                   └───────────┬────────────┘
                                               │ 1
                                               │
                                               │ 1
                                   ┌───────────v────────────┐
                                   │      ReviewReport      │
                                   ├────────────────────────┤
                                   │ id (PK)                │
                                   │ pull_request_id (FK)   │
                                   │ overall_score (Int)    │
                                   │ summary (Text)         │
                                   │ created_at (DateTime)  │
                                   └───────────┬────────────┘
                                               │ 1
                                               │
                                               │ *
                                   ┌───────────v────────────┐
                                   │        Finding         │
                                   ├────────────────────────┤
                                   │ id (PK)                │
                                   │ review_report_id (FK)  │
                                   │ severity (Enum)        │
                                   │ category (Enum)        │
                                   │ file_path (String)     │
                                   │ line_start (Integer)   │
                                   │ line_end (Integer)     │
                                   │ title (String)         │
                                   │ description (Text)     │
                                   │ why_it_matters (Text)  │
                                   │ suggested_fix (Text)   │
                                   │ confidence (Float)     │
                                   └────────────────────────┘
```

---

## 8. Security & Vulnerability Model

- **Read-Only Operation**: CodeGuard AI never modifies, closes, or commits to user repositories automatically.
- **No Hardcoded Credentials**: API tokens (`GITHUB_TOKEN`, `AI_API_KEY`) are fetched strictly from runtime environment variables.
- **Input Sanitization**: GitHub repository names, PR numbers, and user inputs are strictly validated against regex patterns to prevent command or URL injection.
- **Untrusted Code Sandbox**: Repository code diffs are treated as untrusted text strings; code execution of PR content is strictly prohibited.
- **Schema Validation**: All AI provider raw text outputs are parsed through Pydantic v2 schemas; invalid JSON payloads are rejected gracefully.

---

## 9. Deployment & CI/CD Architecture

- **Local Execution**: Backend runs on `http://localhost:8000`, Frontend on `http://localhost:5173`.
- **CI/CD Pipeline**: GitHub Actions (`.github/workflows/ci.yml`):
  1. Installs Python & Node dependencies.
  2. Runs Python `ruff` linting/formatting checks, and `pytest` test suite with coverage enforcement (minimum 85%).
  3. Runs Frontend `oxlint` linting, `vitest` unit tests, and Vite production build.
  4. Runs Playwright E2E integration tests against the live FastAPI background server using `MockAIProvider`.
