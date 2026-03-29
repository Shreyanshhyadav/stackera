import logging
from datetime import datetime, timedelta
from typing import List, Dict
from collections import deque

logger = logging.getLogger(__name__)


class PriceHistory:
    """In-memory price history storage with configurable retention."""
    
    def __init__(self, max_records_per_symbol: int = 1000):
        self.max_records = max_records_per_symbol
        self.history: Dict[str, deque] = {}
    
    def add_price(self, symbol: str, price_info: dict):
        """Add price record to history."""
        if symbol not in self.history:
            self.history[symbol] = deque(maxlen=self.max_records)
        
        self.history[symbol].append(price_info)
    
    def get_history(self, symbol: str, limit: int = 100) -> List[dict]:
        """Get price history for a symbol."""
        if symbol not in self.history:
            return []
        
        return list(self.history[symbol])[-limit:]
    
    def get_price_stats(self, symbol: str, minutes: int = 60) -> dict:
        """Get price statistics for a symbol in the last N minutes."""
        if symbol not in self.history:
            return {}
        
        history = list(self.history[symbol])
        if not history:
            return {}
        
        cutoff_time = datetime.fromisoformat(history[-1]["timestamp"]) - timedelta(minutes=minutes)
        recent = [p for p in history if datetime.fromisoformat(p["timestamp"]) >= cutoff_time]
        
        if not recent:
            return {}
        
        prices = [p["price"] for p in recent]
        
        return {
            "symbol": symbol,
            "high": max(prices),
            "low": min(prices),
            "avg": sum(prices) / len(prices),
            "count": len(recent),
            "period_minutes": minutes
        }
    
    def clear_old_records(self, older_than_hours: int = 24):
        """Clear records older than specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        
        for symbol in self.history:
            self.history[symbol] = deque(
                (p for p in self.history[symbol] 
                 if datetime.fromisoformat(p["timestamp"]) >= cutoff_time),
                maxlen=self.max_records
            )
        
        logger.info(f"Cleared price history older than {older_than_hours} hours")


# Global history instance
price_history = PriceHistory()
