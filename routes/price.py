from fastapi import APIRouter, HTTPException, Request

from binance_listener import price_data
from rate_limiter import rate_limiter
from database import price_history
from config import RATE_LIMIT_ENABLED

router = APIRouter(tags=["price"])


def get_client_id(request: Request) -> str:
    """Extract client ID from request."""
    return request.client.host if request.client else "unknown"


@router.get("/price")
async def get_price(symbol: str = "BTCUSDT", request: Request = None):
    """Get latest price for a symbol."""
    if RATE_LIMIT_ENABLED and request:
        client_id = get_client_id(request)
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    symbol = symbol.upper()
    if symbol in price_data:
        return price_data[symbol]
    
    raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")


@router.get("/prices")
async def get_all_prices(request: Request = None):
    """Get all latest prices."""
    if RATE_LIMIT_ENABLED and request:
        client_id = get_client_id(request)
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return price_data


@router.get("/history/{symbol}")
async def get_price_history(symbol: str, limit: int = 100, request: Request = None):
    """Get price history for a symbol."""
    if RATE_LIMIT_ENABLED and request:
        client_id = get_client_id(request)
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    symbol = symbol.upper()
    history = price_history.get_history(symbol, limit)
    
    if not history:
        raise HTTPException(status_code=404, detail=f"No history for {symbol}")
    
    return {"symbol": symbol, "history": history}


@router.get("/stats/{symbol}")
async def get_price_stats(symbol: str, minutes: int = 60, request: Request = None):
    """Get price statistics for a symbol."""
    if RATE_LIMIT_ENABLED and request:
        client_id = get_client_id(request)
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    symbol = symbol.upper()
    stats = price_history.get_price_stats(symbol, minutes)
    
    if not stats:
        raise HTTPException(status_code=404, detail=f"No stats for {symbol}")
    
    return stats
