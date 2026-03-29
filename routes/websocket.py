import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from binance_listener import price_data
from connection_manager import ConnectionManager
from metrics import metrics
from config import MAX_CONNECTIONS

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])

# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for clients to receive price updates."""
    # Check connection limit
    if metrics.current_clients >= MAX_CONNECTIONS:
        await websocket.close(code=1008, reason="Server at max capacity")
        return
    
    await manager.connect(websocket, price_data)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        metrics.record_error()
        await manager.disconnect(websocket)


def get_manager():
    """Get the connection manager instance."""
    return manager
