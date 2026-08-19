# MediMind AI — Testing

## Status: Phase 0
Current tests: `backend/tests/test_health.py` — confirms the FastAPI app boots
and the `/api/v1/health` route responds. Run with:

```bash
cd backend
python3 -m pytest tests/ -v
```

## Strategy going forward
- Every new API endpoint gets at least one happy-path test and one
  auth/permission-failure test.
- Security-sensitive features (auth, record access) get explicit
  "Patient A cannot see Patient B's data" tests.
- AI modules get a small hand-labeled evaluation set (documented in `AI.md`),
  not just anecdotal spot-checks.
- Frontend gets component tests for critical flows starting Phase 1 (login).
