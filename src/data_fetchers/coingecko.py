"""CoinGecko API data fetcher - Free tier, no API key needed."""

import logging
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


class CoinGeckoFetcher:
    """Fetches price and market data from CoinGecko (free tier)."""
    
    def __init__(self, timeout: int = 10):
        self.base_url = COINGECKO_BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current BTC price in USDT.
        
        Args:
            symbol: Crypto ID (e.g., 'bitcoin')
        
        Returns:
            Current price in USDT or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/simple/price"
            params = {
                'ids': symbol.lower(),
                'vs_currencies': 'usd',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
            }
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            price = data.get(symbol.lower(), {}).get('usd')
            logger.debug(f"Fetched {symbol} price: ${price}")
            return price
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {symbol} price: {e}")
            return None
    
    def get_ohlcv(self, symbol: str, days: int = 7) -> Optional[List]:
        """Get historical OHLCV data.
        
        Args:
            symbol: Crypto ID (e.g., 'bitcoin')
            days: Number of days of history
        
        Returns:
            List of OHLCV candles or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/coins/{symbol.lower()}/ohlc"
            params = {'vs_currency': 'usd', 'days': days}
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Fetched {len(data)} candles for {symbol}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch OHLCV for {symbol}: {e}")
            return None
    
    def get_market_data(self, symbol: str) -> Optional[Dict]:
        """Get comprehensive market data.
        
        Args:
            symbol: Crypto ID (e.g., 'bitcoin')
        
        Returns:
            Market data dict or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/coins/{symbol.lower()}"
            params = {'localization': 'false'}
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Fetched market data for {symbol}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch market data for {symbol}: {e}")
            return None
