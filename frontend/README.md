# CodeGuard AI Frontend

React + TypeScript + Vite frontend for the CodeGuard AI platform. Provides a dark-mode dashboard for submitting PR URLs, viewing real-time multi-agent analysis progress, and exploring actionable review findings.

## Tech Stack

- **React 19** with TypeScript (strict mode)
- **Vite 8** — Fast build tool and dev server
- **Tailwind CSS 4** — Utility-first styling
- **Axios** — HTTP client for API communication
- **Lucide React** — Icon library
- **Vitest** — Unit testing
- **Playwright** — End-to-end testing
- **Oxlint** — Fast TypeScript/React linter

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components (FindingCard, SeverityPill, etc.)
│   ├── context/         # React Context providers (ThemeContext)
│   ├── pages/           # Page components (DashboardPage, PRReviewPage)
│   ├── services/        # API client (api.ts)
│   ├── types/           # TypeScript interfaces (review.ts)
│   ├── App.tsx          # Root component with routing
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles & Tailwind imports
├── e2e/                 # Playwright E2E tests
├── public/              # Static assets
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
├── playwright.config.ts # Playwright configuration
├── .oxlintrc.json       # Oxlint configuration
└── .env.example         # Environment variable template
```

## Quick Start

### Prerequisites

- Node.js 18+
- npm
- Backend server running (see [Backend README](../backend/README.md))

### Installation

```bash
cd frontend

# Install dependencies
npm install
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (default points to http://localhost:8000)
```

### Development

```bash
# Start dev server with HMR
npm run dev
```

The dashboard will be available at **http://localhost:5173**.

### Production Build

```bash
# Type-check and build for production
npm run build

# Preview production build locally
npm run preview
```

Output goes to `dist/` directory.

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Type-check + production build |
| `npm run lint` | Run Oxlint |
| `npm run preview` | Preview production build |
| `npm run test:e2e` | Run Playwright E2E tests |

## Environment Variables

See `.env.example`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_BASE_URL` | No | `http://localhost:8000` | Backend API base URL |

## Key Features

- **Dashboard**: Submit GitHub PR URLs or load sample PRs
- **Real-time Progress**: Live pipeline status during multi-agent analysis
- **PR Health Score**: Aggregate score with severity breakdown
- **Interactive Findings**: Filterable, searchable findings with code context
- **One-click Copy**: Copy suggested fixes directly to clipboard
- **Dark Mode**: Persisted theme preference

## Testing

### Unit Tests (Vitest)

```bash
# Run unit tests
npm run test

# Run with coverage
npm run test -- --coverage
```

### E2E Tests (Playwright)

```bash
# Install browsers (first time only)
npx playwright install

# Run all E2E tests
npm run test:e2e

# Run with UI mode
npx playwright test --ui

# Run specific test
npx playwright test e2e/review_flow.spec.ts
```

## Linting

```bash
# Check code style
npm run lint

# Oxlint configuration in .oxlintrc.json
```

## API Integration

The frontend communicates with the backend via `src/services/api.ts` using Axios. The base URL is configured via `VITE_API_BASE_URL`.

## Project Architecture

See [System Architecture](../docs/architecture.md) and [Agent Constitution](../AGENTS.md) for detailed documentation.