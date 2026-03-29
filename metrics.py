import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)


class Metrics:
    """Track application metrics for monitoring."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.total_messages_received = 0
        self.total_messages_sent = 0
        self.total_clients_connected = 0
        self.current_clients = 0
        self.errors_count = 0
        self.last_binance_update = None
        self.binance_connection_attempts = 0
    
    def record_message_received(self):
        """Record incoming message from Binance."""
        self.total_messages_received += 1
        self.last_binance_update = datetime.now()
    
    def record_message_sent(self):
        """Record outgoing message to client."""
        self.total_messages_sent += 1
    
    def record_client_connected(self):
        """Record new client connection."""
        self.total_clients_connected += 1
        self.current_clients += 1
    
    def record_client_disconnected(self):
        """Record client disconnection."""
        self.current_clients = max(0, self.current_clients - 1)
    
    def record_error(self):
        """Record an error."""
        self.errors_count += 1
    
    def record_binance_connection_attempt(self):
        """Record Binance connection attempt."""
        self.binance_connection_attempts += 1
    
    def get_stats(self) -> Dict:
        """Get current metrics."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "uptime_seconds": uptime,
            "total_messages_received": self.total_messages_received,
            "total_messages_sent": self.total_messages_sent,
            "total_clients_connected": self.total_clients_connected,
            "current_clients": self.current_clients,
            "errors_count": self.errors_count,
            "last_binance_update": self.last_binance_update.isoformat() if self.last_binance_update else None,
            "binance_connection_attempts": self.binance_connection_attempts,
            "messages_per_second": self.total_messages_received / uptime if uptime > 0 else 0
        }


metrics = Metrics()
