import logging
from typing import Set

from fastapi import WebSocket

from metrics import metrics

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket client connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket, price_data: dict):
        """Register a new client connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        metrics.record_client_connected()
        logger.info(f"Client connected. Total clients: {len(self.active_connections)}")
        
        # Send current prices to new client
        for symbol, data in price_data.items():
            await websocket.send_json(data)
            metrics.record_message_sent()
    
    async def disconnect(self, websocket: WebSocket):
        """Remove a client connection."""
        self.active_connections.discard(websocket)
        metrics.record_client_disconnected()
        logger.info(f"Client disconnected. Total clients: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
                metrics.record_message_sent()
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                metrics.record_error()
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            await self.disconnect(conn)
