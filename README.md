# MediMind AI — An AI-Powered Digital Hospital Assistant

**Tagline:** Smarter Healthcare. Connected Care.

MediMind AI is a digital hospital platform connecting patients, doctors, and
administrators, with AI assistance layered on top of a real hospital system
(appointments, medical records, prescriptions). The AI is an **assistant**,
never a replacement for a licensed medical professional — see `docs/AI.md`
and `docs/SECURITY.md` once those are written in later phases.

## Current status: Phase 0 — Project Foundation

This repo currently contains the skeleton only:
- Backend: FastAPI app with a working `/health` and `/health/db` endpoint.
- Frontend: Next.js app with a placeholder landing page that pings the backend.
- Database: PostgreSQL running via Docker, no tables yet (Phase 1 adds the first model).
- Docker Compose wiring all three together for local development.

No authentication, no hospital features, no AI yet — those come in later phases.

## Project structure

```
medimind-ai/
├── frontend/     # Next.js (TypeScript, Tailwind)
├── backend/      # FastAPI (Python)
├── database/     # Alembic migrations + seed data (added from Phase 1)
├── infra/        # Docker Compose, Dockerfiles
├── docs/         # Architecture, API, security, roadmap docs
└── README.md
```

## Prerequisites

- Docker Desktop (or Docker Engine + Compose)
- Git
- Node.js 20+ (optional locally — only needed if you want to run the frontend
  outside Docker)
- Python 3.12+ (optional locally — only needed if you want to run the backend
  outside Docker)

## Quick start (Docker — recommended)

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd medimind-ai

# 2. Create your local env file from the example
cp infra/.env.example .env

# 3. Start everything
docker compose -f infra/docker-compose.yml --env-file .env up --build
```

Then open:
- Frontend: http://localhost:3000
- Backend docs (Swagger UI): http://localhost:8000/docs
- Backend health check: http://localhost:8000/api/v1/health
- Backend DB health check: http://localhost:8000/api/v1/health/db

If the frontend page shows **Backend API status: connected**, Phase 0 is working.

## Running without Docker (alternative, for local debugging)

**Backend:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

You'll need a local PostgreSQL instance running and `DATABASE_URL` set in
`backend/.env` for `/health/db` to succeed in this mode.

## Documentation

See the `docs/` folder:
- `ARCHITECTURE.md` — full system architecture
- `DATABASE.md` — schema, updated per phase
- `API.md` — API conventions and endpoint list
- `AI.md` — AI module design and safety rules
- `SECURITY.md` — auth, access control, data protection rules
- `DEPLOYMENT.md` — how we deploy
- `TESTING.md` — testing strategy and how to run tests
- `PROJECT_ROADMAP.md` — phase-by-phase plan and current status

## Team

| Member | Primary responsibility |
|---|---|
| Member 1 | AI/ML (LLM integration, OCR, RAG, voice, AI safety) |
| Member 2 | Backend, database, DevOps, security |
| Member 3 | Frontend (Next.js, dashboards, UI/UX) |

## Development rule

We build in phases (see `PROJECT_ROADMAP.md`). Do not merge features from a
later phase before the current phase's features are working and tested.
