# AGENTS.md — Agent Rules & Constitution for CodeGuard AI

This document establishes the binding rules, coding standards, architecture constraints, and behavioral principles for AI agents and human developers contributing to the **CodeGuard AI** platform repository.

---

## 1. Core Principles & Philosophy

1. **Non-Hallucination & Evidence First**: AI agents must never invent non-existent files, line numbers, or security vulnerabilities. Every reported finding must be backed by concrete evidence from the git diff context.
2. **Determinism over Randomness**: Agent outputs, severity ratings, and API responses must be deterministic. High confidence thresholds (>= 0.70) are enforced before presenting findings to users.
3. **Information Density & Developer Utility**: The UI and agent summaries must be direct, technical, and actionable. Avoid conversational pleasantries, generic chatbot filler, or bloated visual fluff.
4. **Read-Only Scope**: CodeGuard AI acts strictly as an analytical advisor. Agents must never attempt to mutate, merge, or close user GitHub pull requests.

---

## 2. Architecture Rules

- **Strict Component Isolation**:
  - `frontend/`: UI components, state management, and Playwright tests. Must not contain backend business logic.
  - `backend/app/api/`: REST API routing only. Must delegate parsing, logic, and AI execution to services and agents.
  - `backend/app/services/`: Reusable stateless services (`GitHubService`, `DiffParser`, `AIProvider`).
  - `backend/app/agents/`: Domain-specific AI agents inheriting from `BaseAgent`.
- **AI Provider Abstraction**:
  - Code must NEVER directly instantiate LLM clients inside API endpoints or agents.
  - All LLM queries MUST pass through the `AIProvider` interface.
- **Pydantic Schema Enforcement**:
  - All LLM outputs MUST be parsed and validated against Pydantic v2 schemas (`PRReviewResponse`, `FindingSchema`).

---

## 3. Coding Standards & Conventions

### Python (Backend)
- **Version**: Python 3.11+ using standard type hints (`str`, `int`, `list[str]`, `dict[str, Any]`).
- **Formatting & Style**: Follow PEP 8 guidelines. Use `snake_case` for functions/variables and `PascalCase` for classes.
- **Async First**: Use `async`/`await` for all I/O operations (FastAPI endpoints, httpx GitHub calls, database queries).
- **Docstrings**: Include clear Google-style docstrings for public classes and functions.

### TypeScript / React (Frontend)
- **TypeScript**: Strict mode enabled (`strict: true`). Avoid using `any`; define explicit interfaces in `src/types/`.
- **Components**: Functional React components with named exports (`export const FindingCard = ...`).
- **Styling**: Tailwind CSS class utilities. Avoid inline `style={...}` objects unless dynamically computing layout dimensions.

---

## 4. Security Rules

- **Zero Secrets in Code**: Never hardcode secrets, API keys, or tokens (`GITHUB_TOKEN`, `AI_API_KEY`, `DATABASE_URL`).
- **Git Hygiene**: `.env` files must be listed in `.gitignore`. Commit `.env.example` with dummy values.
- **Input Validation**: All external inputs (GitHub URLs, repository strings, PR numbers) must be validated and sanitized before making outgoing HTTP calls.
- **Sandboxed Diff Inspection**: Git diffs must be processed as untrusted text strings. Code execution of incoming PR patches is strictly forbidden.

---

## 5. Testing Requirements

- **Backend Unit Tests**:
  - Minimum 85% test coverage using `pytest`.
  - All tests MUST execute against `MockAIProvider` to guarantee deterministic, offline execution in CI pipelines.
- **Frontend & E2E Tests**:
  - Component tests with Vitest / React Testing Library where applicable.
  - Playwright E2E tests covering full submission, review generation, severity filtering, and finding detail inspection.

---

## 6. Error Handling & Resilience

- **Graceful Schema Failure**: If an AI provider returns malformed output that fails schema validation, the agent must catch `ValidationError`, log the raw output, and return a fallback finding object instead of crashing.
- **HTTP Status Codes**: Use standard HTTP status codes:
  - `200 OK`: Successful review query / health check.
  - `400 Bad Request`: Invalid GitHub URL or malformed payload.
  - `404 Not Found`: Repository or PR not found on GitHub.
  - `500 Internal Server Error`: Unhandled system failure.

---

## 7. Git & Commit Guidelines

- **Commit Message Format**: Follow Conventional Commits:
  - `feat(scope): add new feature`
  - `fix(scope): fix bug`
  - `test(scope): add unit/E2E test`
  - `docs(scope): update documentation`
  - `ci(scope): update GitHub Actions workflow`
- **Progressive Commits**: Commit incrementally after completing logical milestones. Never create single monolithic commits.
