from fastapi import APIRouter, HTTPException, Request

from metrics import metrics
from rate_limiter import rate_limiter
from config import RATE_LIMIT_ENABLED

router = APIRouter(tags=["metrics"])


def get_client_id(request: Request) -> str:
    """Extract client ID from request."""
    return request.client.host if request.client else "unknown"


@router.get("/metrics")
async def get_metrics(request: Request = None):
    """Get application metrics."""
    if RATE_LIMIT_ENABLED and request:
        client_id = get_client_id(request)
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return metrics.get_stats()
