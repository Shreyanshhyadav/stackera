import os
from dotenv import load_dotenv

load_dotenv()

# Binance Configuration
BINANCE_WS_URL = os.getenv("BINANCE_WS_URL", "wss://stream.binance.com:9443/ws")
CRYPTO_PAIRS = os.getenv("CRYPTO_PAIRS", "btcusdt,ethusdt,bnbusdt").split(",")

# Server Configuration
LOCAL_WS_PORT = int(os.getenv("LOCAL_WS_PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# Rate Limiting
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", 60))

# Connection Limits
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 100))

# Database (optional)
DATABASE_URL = os.getenv("DATABASE_URL", None)
ENABLE_HISTORY = os.getenv("ENABLE_HISTORY", "false").lower() == "true"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
