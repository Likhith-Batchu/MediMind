# MediMind AI — Architecture

See the full architecture discussion doc for the complete reasoning behind
every decision below (tech stack tradeoffs, rejected alternatives, risks).
This file is the living, evolving summary — update it at the end of every
phase.

## Stack
- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI (Python), modular monolith (routes → services → repositories)
- Database: PostgreSQL (+ pgvector from Phase 7 onward)
- Object storage: S3-compatible (MinIO locally)
- AI: LLM API + Sentence-Transformers + Tesseract OCR, called from `backend/app/ai/`
- Infra: Docker Compose (local), GitHub Actions (CI/CD from Phase 10)

## High-level flow
```
Frontend → Backend API → Services → Repositories → PostgreSQL / Object Storage
                       → AI module (called server-side only, never from frontend directly)
```

## Why a modular monolith, not microservices
Three students, nine months. A single well-organized FastAPI app with clear
internal module boundaries is easier to build, test, deploy, and debug than
a distributed system. We revisit this only if we hit a concrete scaling wall.

_(This file will be expanded phase by phase — e.g. DB schema diagrams added
after Phase 1/2/3, AI pipeline diagrams added after Phase 4-8.)_
