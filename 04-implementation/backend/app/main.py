from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import routes_programmes, routes_jobs, routes_analysis, routes_reports

app = FastAPI(
    title="Iris — Skill Gap Analysis API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_programmes.router, prefix="/programmes", tags=["programmes"])
app.include_router(routes_jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(routes_analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(routes_reports.router, prefix="/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
