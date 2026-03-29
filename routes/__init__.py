from fastapi import APIRouter
from .health import router as health_router
from .price import router as price_router
from .websocket import router as websocket_router
from .metrics import router as metrics_router

def include_routes(app):
    """Include all route routers in the app."""
    app.include_router(health_router)
    app.include_router(price_router)
    app.include_router(websocket_router)
    app.include_router(metrics_router)
