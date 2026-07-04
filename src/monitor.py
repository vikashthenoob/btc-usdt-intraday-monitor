"""Main application orchestrator for BTC/USDT intraday monitoring."""

import logging
import asyncio
from typing import Dict, Optional
from datetime import datetime, timedelta
import json

from src.data_fetchers.bybit import BybitFetcher
from src.indicators.calculator import IndicatorCalculator
from src.alerts.alert_manager import AlertManager, AlertRuleEngine, AlertSeverity, AlertType

logger = logging.getLogger(__name__)


class IntradrDayMonitor:
    """Main orchestrator for intraday BTC/USDT monitoring and analysis."""
    
    def __init__(
        self,
        symbol: str = 'BTCUSDT',
        check_interval: int = 60,
        sma_period: int = 20,
        rsi_period: int = 14,
        bollinger_period: int = 20
    ):
        """Initialize the monitor.
        
        Args:
            symbol: Trading symbol to monitor
            check_interval: Seconds between checks
            sma_period: SMA period for calculations
            rsi_period: RSI period for calculations
            bollinger_period: Bollinger Bands period
        """
        self.symbol = symbol
        self.check_interval = check_interval
        self.sma_period = sma_period
        self.rsi_period = rsi_period
        self.bollinger_period = bollinger_period
        
        # Initialize components
        self.fetcher = BybitFetcher()
        self.alert_manager = AlertManager()
        self.rule_engine = AlertRuleEngine(self.alert_manager)
        self.calculator = IndicatorCalculator()
        
        # State tracking
        self.price_history: Dict[str, list] = {
            'timestamps': [],
            'opens': [],
            'highs': [],
            'lows': [],
            'closes': [],
            'volumes': []
        }
        self.current_state = {}
        self.running = False
    
    async def fetch_market_data(self) -> Optional[Dict]:
        """Fetch current market data from Bybit.
        
        Returns:
            Market data dictionary or None if fetch fails
        """
        try:
            ticker_data = self.fetcher.get_tickers(self.symbol)
            funding_rate = self.fetcher.get_funding_rate(self.symbol)
            open_interest = self.fetcher.get_open_interest(self.symbol)
            liquidations = self.fetcher.get_liquidation_data(self.symbol, limit=50)
            
            if not ticker_data:
                logger.warning("Failed to fetch ticker data")
                return None
            
            result = ticker_data.get('list', [{}])[0] if ticker_data.get('list') else {}
            
            return {
                'timestamp': datetime.utcnow(),
                'price': float(result.get('lastPrice', 0)),
                'high_24h': float(result.get('highPrice24h', 0)),
                'low_24h': float(result.get('lowPrice24h', 0)),
                'volume_24h': float(result.get('volume24h', 0)),
                'funding_rate': funding_rate,
                'open_interest': open_interest,
                'liquidations': liquidations
            }
        
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return None
    
    def update_price_history(self, market_data: Dict) -> None:
        """Update price history with new market data.
        
        Args:
            market_data: Current market data
        """
        self.price_history['timestamps'].append(market_data['timestamp'])
        self.price_history['closes'].append(market_data['price'])
        self.price_history['highs'].append(market_data['high_24h'])
        self.price_history['lows'].append(market_data['low_24h'])
        self.price_history['volumes'].append(market_data['volume_24h'])
        
        # Keep only last 500 data points to manage memory
        max_history = 500
        for key in self.price_history:
            if len(self.price_history[key]) > max_history:
                self.price_history[key] = self.price_history[key][-max_history:]
    
    def calculate_indicators(self) -> Dict:
        """Calculate technical indicators from price history.
        
        Returns:
            Dictionary of calculated indicators
        """
        if len(self.price_history['closes']) < self.bollinger_period:
            return {}
        
        closes = self.price_history['closes']
        highs = self.price_history['highs']
        lows = self.price_history['lows']
        
        indicators = {}
        
        # SMA
        sma = self.calculator.sma(closes, self.sma_period)
        indicators['sma'] = sma[-1] if sma[-1] is not None else None
        
        # EMA
        ema = self.calculator.ema(closes, self.sma_period)
        indicators['ema'] = ema[-1] if ema[-1] is not None else None
        
        # RSI
        rsi = self.calculator.rsi(closes, self.rsi_period)
        indicators['rsi'] = rsi[-1] if rsi[-1] is not None else None
        
        # MACD
        macd_line, signal_line, histogram = self.calculator.macd(closes)
        indicators['macd'] = macd_line[-1] if macd_line[-1] is not None else None
        indicators['macd_signal'] = signal_line[-1] if signal_line[-1] is not None else None
        indicators['macd_histogram'] = histogram[-1] if histogram[-1] is not None else None
        
        # Bollinger Bands
        upper, middle, lower = self.calculator.bollinger_bands(closes, self.bollinger_period)
        indicators['bb_upper'] = upper[-1] if upper[-1] is not None else None
        indicators['bb_middle'] = middle[-1] if middle[-1] is not None else None
        indicators['bb_lower'] = lower[-1] if lower[-1] is not None else None
        
        # ATR
        atr = self.calculator.atr(highs, lows, closes)
        indicators['atr'] = atr[-1] if atr[-1] is not None else None
        
        return indicators
    
    def evaluate_conditions(self, market_data: Dict, indicators: Dict) -> None:
        """Evaluate trading conditions and trigger alerts.
        
        Args:
            market_data: Current market data
            indicators: Calculated indicators
        """
        price = market_data['price']
        
        # Check RSI levels
        if indicators.get('rsi') is not None:
            self.rule_engine.check_rsi_levels(
                self.symbol,
                indicators['rsi'],
                price
            )
        
        # Check Bollinger Bands
        if indicators.get('bb_upper') and indicators.get('bb_lower'):
            self.rule_engine.check_bollinger_bands(
                self.symbol,
                price,
                indicators['bb_upper'],
                indicators['bb_lower']
            )
        
        # Check liquidation spikes
        liquidations = market_data.get('liquidations', [])
        if liquidations:
            total_liquidation = sum(float(l.get('size', 0)) for l in liquidations)
            self.rule_engine.check_liquidation_spike(
                self.symbol,
                total_liquidation,
                threshold=1000000,  # 1M USDT threshold
                price=price
            )
    
    def get_current_state(self) -> Dict:
        """Get current market state and indicators.
        
        Returns:
            Dictionary with current state
        """
        return {
            'symbol': self.symbol,
            'timestamp': datetime.utcnow().isoformat(),
            'price_history_length': len(self.price_history['closes']),
            'indicators': self.current_state.get('indicators', {}),
            'critical_alerts': len(self.alert_manager.get_critical_alerts(self.symbol)),
            'total_alerts': len(self.alert_manager.alerts)
        }
    
    async def run_check(self) -> None:
        """Execute single monitoring check cycle."""
        try:
            # Fetch market data
            market_data = await asyncio.to_thread(self.fetch_market_data)
            if not market_data:
                logger.warning("Skipping check due to failed data fetch")
                return
            
            # Update history
            self.update_price_history(market_data)
            
            # Calculate indicators
            indicators = self.calculate_indicators()
            
            # Evaluate conditions
            self.evaluate_conditions(market_data, indicators)
            
            # Update state
            self.current_state = {
                'market_data': market_data,
                'indicators': indicators,
                'timestamp': datetime.utcnow()
            }
            
            logger.debug(f"Check complete. Price: {market_data['price']}, Alerts: {len(self.alert_manager.alerts)}")
        
        except Exception as e:
            logger.error(f"Error during check: {e}")
    
    async def start(self) -> None:
        """Start continuous monitoring loop."""
        self.running = True
        logger.info(f"Starting monitor for {self.symbol}")
        
        try:
            while self.running:
                await self.run_check()
                await asyncio.sleep(self.check_interval)
        
        except asyncio.CancelledError:
            logger.info("Monitor cancelled")
        except Exception as e:
            logger.error(f"Monitor error: {e}")
        finally:
            self.running = False
    
    def stop(self) -> None:
        """Stop monitoring."""
        self.running = False
        logger.info("Monitor stopped")
    
    def get_alerts_summary(self) -> Dict:
        """Get summary of current alerts.
        
        Returns:
            Summary dictionary
        """
        all_alerts = self.alert_manager.alerts
        critical = self.alert_manager.get_critical_alerts(self.symbol)
        
        return {
            'total_alerts': len(all_alerts),
            'critical_alerts': len(critical),
            'recent_alerts': [a.to_dict() for a in self.alert_manager.get_alerts(self.symbol, limit=10)],
            'alert_types': list(set(a.alert_type.value for a in all_alerts))
        }


async def main():
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    
    monitor = IntradrDayMonitor(check_interval=60)
    
    try:
        await monitor.start()
    except KeyboardInterrupt:
        monitor.stop()


if __name__ == '__main__':
    asyncio.run(main())
