import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Include all routes
include_routes(app)

# Set lifespan
app.router.lifespan_context = lifespan


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=LOCAL_WS_PORT, log_level=LOG_LEVEL.lower())
