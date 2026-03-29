from fastapi import APIRouter

from metrics import metrics

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": metrics.start_time.isoformat(),
        "active_clients": metrics.current_clients
    }
