#!/usr/bin/env python3
"""
BTC/USDT Intraday Movement Monitor - Main Entry Point

Monitors Bitcoin intraday price movements tracking the top 10 drivers:
1. Order-book Liquidity Shocks
2. Order Flow Imbalance (VPIN)
3. Futures Funding Rate Extremes
4. Open Interest Jumps/Drops
5. Liquidation Clusters
6. Exchange Net Flows
7. Whale Transfers
8. News/Social Spikes
9. Cross-Market Triggers
10. Technical Thresholds

Usage:
    python main.py --config config.yaml
    python main.py --symbol BTCUSDT --interval 5m
"""

import asyncio
import logging
import argparse
from pathlib import Path
from datetime import datetime

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/monitor.log')
    ]
)
logger = logging.getLogger(__name__)


class IntraDayMonitor:
    """Main monitoring system for BTC/USDT intraday movements."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize monitor with configuration."""
        self.config = self._load_config(config_path)
        self.symbol = self.config.get('symbol', 'BTCUSDT')
        self.interval = self.config.get('interval', '5m')
        logger.info(f"Monitor initialized: {self.symbol} @ {self.interval}")
    
    @staticmethod
    def _load_config(config_path: str) -> dict:
        """Load YAML configuration file."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    
    async def start(self):
        """Start the monitoring loop."""
        logger.info("=" * 60)
        logger.info("Starting BTC/USDT Intraday Monitor")
        logger.info("=" * 60)
        logger.info(f"Symbol: {self.symbol}")
        logger.info(f"Interval: {self.interval}")
        logger.info("")
        logger.info("TOP 10 INTRADAY DRIVERS BEING MONITORED:")
        logger.info("1.  Order-book Liquidity Shocks")
        logger.info("2.  Order Flow Imbalance (VPIN)")
        logger.info("3.  Futures Funding Rate Extremes")
        logger.info("4.  Open Interest Jumps/Drops")
        logger.info("5.  Liquidation Clusters")
        logger.info("6.  Exchange Net Flows")
        logger.info("7.  Whale Transfers")
        logger.info("8.  News/Social Spikes")
        logger.info("9.  Cross-Market Triggers (S&P, DXY)")
        logger.info("10. Technical Thresholds (VWAP, RSI, Bollinger)")
        logger.info("=" * 60)
        
        try:
            while True:
                logger.info(f"[{datetime.now().isoformat()}] Monitoring {self.symbol}...")
                # TODO: Implement actual monitoring logic
                # - Fetch price data from CoinGecko/Binance
                # - Fetch funding rates from Bybit
                # - Compute technical indicators
                # - Check thresholds
                # - Generate alerts
                await asyncio.sleep(self.config.get('data', {}).get('refresh_interval', 60))
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='BTC/USDT Intraday Movement Monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Use default config.yaml
  python main.py --config custom_config.yaml       # Use custom config
  python main.py --symbol BTCUSDT --interval 5m    # Override config values
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        default=None,
        help='Trading symbol (e.g., BTCUSDT)'
    )
    
    parser.add_argument(
        '--interval',
        type=str,
        default=None,
        choices=['1m', '5m', '15m', '1h'],
        help='Candlestick interval (1m, 5m, 15m, 1h)'
    )
    
    args = parser.parse_args()
    
    # Initialize and start monitor
    monitor = IntraDayMonitor(args.config)
    
    # Override config with CLI arguments if provided
    if args.symbol:
        monitor.symbol = args.symbol
    if args.interval:
        monitor.interval = args.interval
    
    # Start monitoring
    asyncio.run(monitor.start())


if __name__ == '__main__':
    main()
