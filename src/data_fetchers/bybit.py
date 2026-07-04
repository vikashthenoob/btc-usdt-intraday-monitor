"""Bybit API data fetcher - Free tier for futures data."""

import logging
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BYBIT_BASE_URL = "https://api.bybit.com/v5"


class BybitFetcher:
    """Fetches futures and derivatives data from Bybit."""
    
    def __init__(self, timeout: int = 10):
        self.base_url = BYBIT_BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
    
    def get_funding_rate(self, symbol: str = 'BTCUSDT') -> Optional[Dict]:
        """Get current funding rate for perpetual futures.
        
        Args:
            symbol: Futures symbol (e.g., 'BTCUSDT')
        
        Returns:
            Funding rate data dict or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/market/funding/history"
            params = {
                'category': 'linear',
                'symbol': symbol,
                'limit': 1,
            }
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if data.get('retCode') == 0:
                result = data.get('result', {})
                logger.debug(f"Fetched funding rate for {symbol}")
                return result
            else:
                logger.error(f"Bybit API error: {data.get('retMsg')}")
                return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch funding rate: {e}")
            return None
    
    def get_open_interest(self, symbol: str = 'BTCUSDT') -> Optional[Dict]:
        """Get open interest data.
        
        Args:
            symbol: Futures symbol (e.g., 'BTCUSDT')
        
        Returns:
            Open interest data or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/market/open-interest"
            params = {
                'category': 'linear',
                'symbol': symbol,
                'intervalTime': '5min',
                'limit': 1,
            }
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if data.get('retCode') == 0:
                result = data.get('result', {})
                logger.debug(f"Fetched open interest for {symbol}")
                return result
            else:
                logger.error(f"Bybit API error: {data.get('retMsg')}")
                return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch open interest: {e}")
            return None
    
    def get_liquidation_data(self, symbol: str = 'BTCUSDT', limit: int = 50) -> Optional[List]:
        """Get recent liquidation data.
        
        Args:
            symbol: Futures symbol (e.g., 'BTCUSDT')
            limit: Number of records (max 500)
        
        Returns:
            List of liquidation records or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/public/liquidation"
            params = {
                'symbol': symbol,
                'limit': min(limit, 500),
            }
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if data.get('retCode') == 0:
                result = data.get('result', {}).get('rows', [])
                logger.debug(f"Fetched {len(result)} liquidation records for {symbol}")
                return result
            else:
                logger.error(f"Bybit API error: {data.get('retMsg')}")
                return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch liquidation data: {e}")
            return None
    
    def get_tickers(self, symbol: str = 'BTCUSDT') -> Optional[Dict]:
        """Get current ticker information.
        
        Args:
            symbol: Futures symbol (e.g., 'BTCUSDT')
        
        Returns:
            Ticker data or None if request fails
        """
        try:
            endpoint = f"{self.base_url}/market/tickers"
            params = {
                'category': 'linear',
                'symbol': symbol,
            }
            
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if data.get('retCode') == 0:
                result = data.get('result', {})
                logger.debug(f"Fetched ticker for {symbol}")
                return result
            else:
                logger.error(f"Bybit API error: {data.get('retMsg')}")
                return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch tickers: {e}")
            return None
