# MediMind AI — Database

## Status: Phase 0
No tables exist yet. This file will be filled in as each phase adds entities:

- Phase 1 adds: `User`
- Phase 2 adds: `Patient`, `Doctor`, `Department`, `DoctorAvailability`, `Appointment`
- Phase 3 adds: `Document`, `MedicalRecord`, `MedicalReport`, `Prescription`, `PrescriptionMedicine`, `Medicine`, `AuditLog`
- Phase 5 adds: `AIReportSummary`
- Phase 6 adds: `Conversation`, `Message`, `AIInteraction`
- Phase 9 adds: any analytics-supporting tables

Migrations are managed with Alembic, stored in `database/migrations/`.

## Local connection
```
postgresql://medimind:medimind@localhost:5432/medimind_db
```
(matches `infra/.env.example` — change credentials in your real `.env`)
