import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def connect_to_server():
    """Connect to local WebSocket server and receive price updates."""
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to server")
            
            async for message in websocket:
                data = json.loads(message)
                symbol = data.get("symbol", "N/A")
                price = data.get("price", "N/A")
                change = data.get("change_24h", "N/A")
                timestamp = data.get("timestamp", "N/A")
                
                print(f"[{timestamp}] {symbol}: ${price} ({change:+.2f}%)")
    
    except Exception as e:
        logger.error(f"Connection error: {e}")


if __name__ == "__main__":
    asyncio.run(connect_to_server())
