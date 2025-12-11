"""API utility routes - health checks and system endpoints."""

from fastapi import APIRouter

from app.utils import utc_now

router = APIRouter(tags=["api"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": utc_now().isoformat(),
    }
