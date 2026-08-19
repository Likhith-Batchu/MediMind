"""
FastAPI application factory.

This file stays intentionally thin — it only wires together config,
middleware, and routers. All real logic lives in services/, all
DB access lives in repositories/, all routes stay thin wrappers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import health

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "MediMind AI API is running. See /docs for API documentation."}
