# Custom Agents & Skills Documentation — CodeGuard AI

This document specifies the custom AI agents and custom skills implemented within the **CodeGuard AI** platform repository, fulfilling Requirement 4 & 5 of the hackathon mandate.

---

## Part 1: Custom AI Agents

CodeGuard AI implements five specialized agents that operate as modular, domain-focused analysis components:

```
                          ┌────────────────────────────┐
                          │    BaseAgent Interface     │
                          └─────────────┬──────────────┘
                                        │
     ┌──────────────────┬───────────────┼───────────────┬──────────────────┐
     │                  │               │               │                  │
     v                  v               v               v                  v
┌─────────┐       ┌───────────┐   ┌───────────┐   ┌───────────┐    ┌──────────────┐
│   Bug   │       │ Security  │   │   Code    │   │   Test    │    │   Review     │
│ Agent   │       │   Agent   │   │ Quality   │   │ Analysis  │    │ Aggregator   │
└─────────┘       └───────────┘   └───────────┘   └───────────┘    └──────────────┘
```

---

### 1. Bug Detection Agent (`BugDetectionAgent`)

- **Purpose**: Specialized in discovering runtime errors, logical flaws, off-by-one errors, and edge-case exceptions in changed PR code.
- **Inputs**:
  - `pr_metadata`: Title, description, target repository, author.
  - `parsed_diff`: Structured git diff containing added/modified files, diff chunks, and line mappings.
- **Outputs**: List of `FindingSchema` objects categorized under `BUG`.
- **Responsibilities**:
  - Inspect changed lines for unhandled null/undefined pointers or missing optional chaining.
  - Detect array index out-of-bounds risks and off-by-one loop conditions.
  - Highlight unhandled exception paths in async I/O or database calls.
  - Verify boundary condition handling (e.g. empty lists, negative inputs, zero values).
- **Constraints**:
  - Must specify file path, line numbers, and exact code context for every finding.
  - Confidence rating must be >= 0.70 to be included in output.
- **Failure Handling**: Catches parsing failures gracefully, returning zero false-positive findings if confidence is insufficient.

---

### 2. Security Review Agent (`SecurityReviewAgent`)

- **Purpose**: Inspects incoming code diffs for OWASP Top 10 vulnerabilities, credential leaks, and unsafe data handling.
- **Inputs**: `pr_metadata`, `parsed_diff`.
- **Outputs**: List of `FindingSchema` objects categorized under `SECURITY`.
- **Responsibilities**:
  - Detect hardcoded secrets, API keys, private keys, or passwords committed in diffs.
  - Identify SQL injection, Command injection, or Cross-Site Scripting (XSS) vectors.
  - Flag unsafe input deserialization or unvalidated external parameters.
  - Inspect dangerous dependency calls or permission misconfigurations.
- **Constraints**:
  - Never output actual raw secret values in descriptions (redact sensitive values as `***`).
  - Severity level must be assigned conservatively (`CRITICAL` for hardcoded keys / injection, `HIGH` for unvalidated inputs).
- **Failure Handling**: Emits fallback high-priority security warnings if potential secret patterns match regex rules even if LLM parsing fails.

---

### 3. Code Quality Agent (`CodeQualityAgent`)

- **Purpose**: Evaluates maintainability, cognitive complexity, code duplication, and structural code smells.
- **Inputs**: `pr_metadata`, `parsed_diff`.
- **Outputs**: List of `FindingSchema` objects categorized under `CODE_QUALITY` or `PERFORMANCE`.
- **Responsibilities**:
  - Identify duplicated logic blocks across changed files.
  - Flag functions with excessive cyclomatic complexity or deep nesting (> 4 indentation levels).
  - Detect bad naming conventions, dead code, or commented-out code blocks.
  - Suggest cleaner abstractions and modern refactoring patterns.
- **Constraints**:
  - Focus exclusively on modified or added lines; avoid flagging unchanged legacy code.
- **Failure Handling**: Retries with simplified prompt if complex diff payloads exceed token windows.

---

### 4. Test Analysis Agent (`TestAnalysisAgent`)

- **Purpose**: Analyzes whether modified/added code branches are backed by appropriate unit/integration tests and recommends missing test cases.
- **Inputs**: `pr_metadata`, `parsed_diff`.
- **Outputs**: List of `FindingSchema` objects categorized under `TESTING` plus concrete test code recommendations.
- **Responsibilities**:
  - Determine if PR diff includes corresponding test file updates (e.g. `.test.ts`, `test_*.py`).
  - Identify untested edge-case branches in new business logic functions.
  - Provide concrete, runnable code snippets for missing unit tests.
- **Constraints**:
  - Recommendations must match the project's testing framework (Pytest for Python, Vitest/Jest for TypeScript).
- **Failure Handling**: Generates general test guidance if specific framework cannot be inferred.

---

### 5. Review Aggregator & Scorer (`ReviewAggregator`)

- **Purpose**: Combines, deduplicates, prioritizes findings from all specialized agents, and computes the overall PR Health Score.
- **Inputs**: Lists of findings from `BugDetectionAgent`, `SecurityReviewAgent`, `CodeQualityAgent`, `TestAnalysisAgent`.
- **Outputs**: Complete `PRReviewResponse` payload containing overall health score (0-100), severity summary breakdown, and sorted findings.
- **Responsibilities**:
  - Remove duplicate findings with overlapping file paths and line ranges.
  - Calculate overall health score formula:
    \[ \text{Score} = \max\left(0, 100 - (30 \times \text{Critical}) - (15 \times \text{High}) - (5 \times \text{Medium}) - (2 \times \text{Low})\right) \]
  - Sort findings deterministically (`CRITICAL` -> `HIGH` -> `MEDIUM` -> `LOW` -> `INFO`).

---

## Part 2: Custom Skill — `PR Review Skill` (`PRReviewSkill`)

### Name
`PRReviewSkill`

### Purpose
The `PRReviewSkill` is a custom, repeatable process engine that defines the step-by-step workflow for ingesting raw GitHub pull request data, parsing git diffs, orchestrating multi-agent inspections, validating outputs, and compiling developer-friendly review reports.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRReviewSkill Workflow                           │
└─────────────────────────────────────────────────────────────────────────┘
  1. Read PR Metadata (Title, Author, Repo, Branches)
  2. Ingest Unified Diff Patch
  3. Filter Out Noise (Lockfiles, Minified Assets, Documentation)
  4. Build Structured Code Change Map (File, Lines, Additions, Deletions)
  5. Trigger Parallel Agent Analysis (Bug, Security, Quality, Testing)
  6. Execute LLM Provider Queries with Pydantic JSON Schemas
  7. Validate & Sanitize AI Findings (Filter Low Confidence < 0.70)
  8. Aggregate & Deduplicate Findings via ReviewAggregator
  9. Compute PR Overall Health Score (0 - 100)
 10. Persist Report to DB & Return Formatted Web Dashboard Payload
```

### Trigger
Triggered via POST request to `/api/v1/review` with payload containing `repo_url` or `owner`, `repo`, and `pr_number`.

### Inputs
- `repo_owner` (string): Owner of the GitHub repository (e.g. `facebook`).
- `repo_name` (string): Name of the GitHub repository (e.g. `react`).
- `pr_number` (integer): Pull request number (e.g. `1024`).
- `ai_provider` (optional): Selected provider instance (`gemini`, `nvidia`, `mock`).

### Outputs
- `PRReviewResponse`: JSON payload containing:
  - `id`: Database record ID.
  - `pr_metadata`: Object with title, author, repo, url, changed_files count.
  - `overall_score`: Integer from 0 to 100.
  - `summary`: High-level summary of review results.
  - `findings_count`: Total count of active findings.
  - `severity_breakdown`: Object with counts for `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.
  - `findings`: Array of validated `Finding` objects.
