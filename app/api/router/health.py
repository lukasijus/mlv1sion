from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}


@router.get("/ready", tags=["Health"])
async def readiness_check():
    return {"status": "ready"}


@router.get("/live", tags=["Health"])
async def liveness_check():
    return {"status": "alive"}


@router.get("/version", tags=["Health"])
async def version_check():
    return {"version": "1.0.0"}


@router.get("/metrics", tags=["Health"])
async def metrics_check():
    return {"metrics": "sample metrics data"}


@router.get("/status", tags=["Health"])
async def status_check():
    return {"status": "all systems operational"}


@router.get("/ping", tags=["Health"])
async def ping_check():
    return {"ping": "pong"}
