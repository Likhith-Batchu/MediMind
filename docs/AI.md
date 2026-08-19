# MediMind AI — AI Modules

## Status: Phase 0
No AI modules are implemented yet (`backend/app/ai/` currently only contains
an empty `__init__.py`). This file will document, per module as it's built:
- pipeline design
- prompts / prompt strategy
- safety layer behavior
- evaluation method and results
- known limitations

## Non-negotiable safety rules (apply to every future AI module)
1. The AI always identifies itself as an assistant, never a diagnosing doctor.
2. Structured AI output is validated against a schema before being trusted or stored.
3. No AI output triggers a sensitive database write without a service-layer check.
4. Urgent/emergency-sounding input gets a fixed "seek immediate care" response path.
5. Every AI interaction is logged (metadata only, never sensitive content) for evaluation.
6. RAG knowledge base sources are manually curated and documented, never scraped blindly.
