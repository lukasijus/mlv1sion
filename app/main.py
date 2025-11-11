# app/main.py
from fastapi import FastAPI
from app.core.observability import metrics_middleware
from app.api.routers import auth, assets, jobs, devices
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware
app.middleware("http")(metrics_middleware)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])


@app.get("/healthz")
async def health():
    return {"status": "ok"}
