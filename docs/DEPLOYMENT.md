# MediMind AI — Deployment

## Status: Phase 0
Nothing is deployed yet. Local development only, via Docker Compose:

```bash
docker compose -f infra/docker-compose.yml --env-file .env up --build
```

Real deployment (managed Postgres, managed object storage, HTTPS, CI/CD)
is planned for Phase 10 and will be documented here when it happens —
this file will never claim a deployment exists before it actually does.
