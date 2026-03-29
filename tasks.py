import asyncio
import logging

from binance_listener import BinanceListener, price_update_queue
from connection_manager import ConnectionManager
from metrics import metrics

logger = logging.getLogger(__name__)

binance_listener = None


async def broadcast_prices(manager: ConnectionManager):
    """Continuously broadcast price updates to all clients."""
    while True:
        try:
            price_info = await price_update_queue.get()
            await manager.broadcast(price_info)
        except Exception as e:
            logger.error(f"Error in broadcast task: {e}")
            await asyncio.sleep(1)

# -------------------------------------------------------------------------

async def start_binance_listener(pairs: list, binance_ws_url: str):
    """Start the Binance WebSocket listener."""
    global binance_listener
    binance_listener = BinanceListener(pairs, binance_ws_url)
    
    while True:
        try:
            metrics.record_binance_connection_attempt()
            await binance_listener.connect()
            await binance_listener.listen()
        except Exception as e:
            logger.error(f"Binance listener error: {e}")
            metrics.record_error()
            await asyncio.sleep(5)

# -----------------------------------------------------------------------

async def stop_binance_listener():
    """Stop the Binance WebSocket listener."""
    if binance_listener:
        await binance_listener.close()
