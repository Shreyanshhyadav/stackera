import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from config import (
    BINANCE_WS_URL, CRYPTO_PAIRS, LOCAL_WS_PORT, HOST, LOG_LEVEL
)
from tasks import start_binance_listener, broadcast_prices, stop_binance_listener
from routes import include_routes
from routes.websocket import get_manager

# Configure logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("Starting application...")
    logger.info(f"Monitoring pairs: {CRYPTO_PAIRS}")
    
    manager = get_manager()
    binance_task = asyncio.create_task(start_binance_listener(CRYPTO_PAIRS, BINANCE_WS_URL))
    broadcast_task = asyncio.create_task(broadcast_prices(manager))
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    binance_task.cancel()
    broadcast_task.cancel()
    await stop_binance_listener()


# Create FastAPI app
app = FastAPI(
    title="Crypto Price WebSocket",
    description="Real-time cryptocurrency price streaming from Binance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
include_routes(app)

# Set lifespan
app.router.lifespan_context = lifespan

# Serve frontend static files in production
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA for any non-API route."""
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=LOCAL_WS_PORT, log_level=LOG_LEVEL.lower())
