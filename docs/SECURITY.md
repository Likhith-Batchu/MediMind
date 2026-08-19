# MediMind AI — Security

## Status: Phase 0
No auth or access control exists yet — this file becomes real starting Phase 1.

## Rules that apply from Phase 1 onward
- Passwords: bcrypt-hashed, never logged or stored in plaintext.
- Auth: JWT access + refresh tokens.
- Authorization: role-based (patient/doctor/admin/receptionist) enforced server-side.
- Ownership checks: patients can only access their own records; doctors only
  access patients they have a care relationship with.
- File access: signed, time-limited URLs only — no public document links.
- Secrets: environment variables only, `.env` is git-ignored, `.env.example`
  has placeholders only.
- Audit logging: every access to a medical record is logged (from Phase 3).
- Logs: never contain medical content, only metadata.
