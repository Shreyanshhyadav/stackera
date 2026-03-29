import asyncio
import json
import logging
from datetime import datetime
from typing import Dict

import aiohttp

from metrics import metrics
from database import price_history

logger = logging.getLogger(__name__)

# Global state
price_data: Dict[str, dict] = {}
price_update_queue: asyncio.Queue = asyncio.Queue()


class BinanceListener:
    """Handles connection to Binance WebSocket and price updates."""
    
    def __init__(self, pairs: list, binance_ws_url: str):
        self.pairs = pairs
        self.binance_ws_url = binance_ws_url
        self.session = None
        self.ws = None
        
    async def connect(self):
        """Connect to Binance WebSocket."""
        self.session = aiohttp.ClientSession()
        
        # Build subscription string for multiple pairs
        streams = "/".join([f"{pair}@ticker" for pair in self.pairs])
        url = f"{self.binance_ws_url}/{streams}"
        
        logger.info(f"Connecting to Binance: {url}")
        self.ws = await self.session.ws_connect(url)
        
    async def listen(self):
        """Listen for price updates from Binance."""
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    await self.process_price_update(data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {self.ws.exception()}")
                    break
        except Exception as e:
            logger.error(f"Error in Binance listener: {e}")
        finally:
            await self.close()
    
    async def process_price_update(self, data: dict):
        """Extract and store price data, then queue for broadcast."""
        try:
            symbol = data.get("s", "").upper()
            price = float(data.get("c", 0))
            change_24h = float(data.get("P", 0))
            timestamp = datetime.now().isoformat()
            
            price_info = {
                "symbol": symbol,
                "price": price,
                "change_24h": change_24h,
                "timestamp": timestamp
            }
            
            price_data[symbol] = price_info
            price_history.add_price(symbol, price_info)
            await price_update_queue.put(price_info)
            
            metrics.record_message_received()
            logger.info(f"Updated {symbol}: ${price} ({change_24h:+.2f}%)")
        except Exception as e:
            logger.error(f"Error processing price update: {e}")
            metrics.record_error()
    
    async def close(self):
        """Close WebSocket connection."""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
