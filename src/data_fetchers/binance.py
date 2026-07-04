"""Binance API data fetcher - Free tier."""

import logging
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BINANCE_BASE_URL = "https://api.binance.com/api/v3"


class BinanceFetcher:
    """Fetches data from Binance public API (no auth needed)."""
    
    def __init__(self, timeout: int = 10):
        self.base_url = BINANCE_BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
    
    def get_klines(self, symbol: str = 'BTCUSDT', interval: str = '5m', limit: int = 100) -> Optional[List]:
        """Get candlestick data (klines).
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            interval: Candlestick interval (1m, 5m, 15m, 1h, etc.)
            limit: Number of candles (max 1000)
        
        Returns:
            List of klines or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': min(limit, 1000),
            }
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Fetched {len(data)} klines for {symbol}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch klines: {e}")
            return None
    
    def get_ticker(self, symbol: str = 'BTCUSDT') -> Optional[Dict]:
        """Get 24h ticker data.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
        
        Returns:
            Ticker data dict or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/ticker/24hr"
            params = {'symbol': symbol}
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Fetched ticker for {symbol}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch ticker: {e}")
            return None
    
    def get_order_book(self, symbol: str = 'BTCUSDT', limit: int = 20) -> Optional[Dict]:
        """Get order book snapshot.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            limit: Number of levels (valid limits: 5, 10, 20, 50, 100, 500, 1000)
        
        Returns:
            Order book dict with 'bids' and 'asks' or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/depth"
            params = {'symbol': symbol, 'limit': limit}
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Fetched order book for {symbol}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch order book: {e}")
            return None
    
    def get_avg_price(self, symbol: str = 'BTCUSDT') -> Optional[float]:
        """Get current average price.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
        
        Returns:
            Average price or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/avgPrice"
            params = {'symbol': symbol}
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            price = float(data.get('price', 0))
            logger.debug(f"Fetched average price for {symbol}: ${price}")
            return price
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch average price: {e}")
            return None
