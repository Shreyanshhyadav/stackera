import logging
from datetime import datetime, timedelta
from typing import Dict
from collections import deque

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter based on IP address."""
    
    def __init__(self, requests_per_period: int = 100, period_seconds: int = 60):
        self.requests_per_period = requests_per_period
        self.period_seconds = period_seconds
        self.requests: Dict[str, deque] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make a request."""
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.period_seconds)
        
        if client_id not in self.requests:
            self.requests[client_id] = deque()
        
        # Remove old requests outside the period--------------
        while self.requests[client_id] and self.requests[client_id][0] < cutoff_time:
            self.requests[client_id].popleft()
        
        # Check if limit exceeded-------------------
        if len(self.requests[client_id]) >= self.requests_per_period:
            logger.warning(f"Rate limit exceeded for client {client_id}")
            return False
        
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client."""
        if client_id not in self.requests:
            return self.requests_per_period
        
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.period_seconds)
        
        # Count valid requests
        valid_requests = sum(1 for req_time in self.requests[client_id] if req_time >= cutoff_time)
        return max(0, self.requests_per_period - valid_requests)


rate_limiter = RateLimiter()
