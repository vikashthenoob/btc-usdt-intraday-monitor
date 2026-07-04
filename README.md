# BTC/USDT Intraday Monitor

A real-time monitoring system for BTC/USDT trading pairs with technical analysis, alert generation, and liquidation tracking.

## Features

### 📊 Technical Analysis
- **Moving Averages**: SMA (Simple Moving Average) and EMA (Exponential Moving Average)
- **RSI (Relative Strength Index)**: Overbought/oversold detection
- **MACD (Moving Average Convergence Divergence)**: Trend confirmation
- **Bollinger Bands**: Volatility and price level analysis
- **ATR (Average True Range)**: Volatility measurement

### 🚨 Alert System
- Real-time price breakout alerts
- RSI overbought/oversold conditions
- MACD crossover signals
- Bollinger Band violations
- Liquidation spike detection
- Funding rate extremes
- Volume surge alerts

### 💰 Market Data
- Real-time price data from Bybit
- Liquidation tracking
- Funding rates
- Open interest
- Volume analysis

### 🔔 Notifications (Optional)
- Discord webhook integration
- Telegram bot support
- Email notifications

## Project Structure

```
btc-usdt-intraday-monitor/
├── src/
│   ├── __init__.py
│   ├── monitor.py                 # Main orchestrator
│   ├── data_fetchers/
│   │   ├── __init__.py
│   │   └── bybit.py              # Bybit API integration
│   ├── indicators/
│   │   ├── __init__.py
│   │   └── calculator.py         # Technical indicators
│   └── alerts/
│       ├── __init__.py
│       └── alert_manager.py      # Alert management system
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/vikashthenoob/btc-usdt-intraday-monitor.git
cd btc-usdt-intraday-monitor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Configuration

Edit `.env` file to customize settings:

### Monitoring Settings
```env
MONITOR_SYMBOL=BTCUSDT          # Trading pair to monitor
CHECK_INTERVAL=60               # Seconds between checks
MAX_PRICE_HISTORY=500           # Price points to keep in history
```

### Indicator Settings
```env
SMA_PERIOD=20                   # Simple Moving Average period
RSI_PERIOD=14                   # RSI period
BOLLINGER_PERIOD=20             # Bollinger Bands period
BOLLINGER_STD_DEV=2.0           # Standard deviations for bands
```

### Alert Thresholds
```env
RSI_OVERBOUGHT=70               # RSI overbought threshold
RSI_OVERSOLD=30                 # RSI oversold threshold
LIQUIDATION_THRESHOLD=1000000   # Liquidation volume threshold (USDT)
FUNDING_RATE_THRESHOLD=0.001    # Funding rate threshold
```

### Notifications (Optional)
```env
ENABLE_NOTIFICATIONS=false
DISCORD_WEBHOOK_URL=your_webhook_url
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Usage

### Starting the Monitor

```bash
python -m src.monitor
```

The monitor will:
1. Connect to Bybit API
2. Fetch market data at regular intervals
3. Calculate technical indicators
4. Evaluate trading conditions
5. Generate alerts when conditions are met

### Programmatic Usage

```python
import asyncio
from src.monitor import IntradrDayMonitor

async def main():
    # Initialize monitor
    monitor = IntradrDayMonitor(
        symbol='BTCUSDT',
        check_interval=60,
        sma_period=20,
        rsi_period=14
    )
    
    # Subscribe to alerts
    from src.alerts.alert_manager import AlertType
    monitor.alert_manager.subscribe(
        AlertType.RSI_OVERBOUGHT,
        lambda alert: print(f"Alert: {alert.message}")
    )
    
    # Start monitoring
    await monitor.start()

if __name__ == '__main__':
    asyncio.run(main())
```

## API Reference

### IndicatorCalculator

```python
from src.indicators.calculator import IndicatorCalculator

calc = IndicatorCalculator()

# SMA
sma_values = calc.sma(prices, period=20)

# RSI
rsi_values = calc.rsi(prices, period=14)

# MACD
macd_line, signal_line, histogram = calc.macd(prices)

# Bollinger Bands
upper, middle, lower = calc.bollinger_bands(prices, period=20)

# ATR
atr_values = calc.atr(highs, lows, closes, period=14)
```

### AlertManager

```python
from src.alerts.alert_manager import AlertManager, AlertType, AlertSeverity

alert_mgr = AlertManager()

# Create alert
alert = alert_mgr.create_alert(
    AlertType.RSI_OVERBOUGHT,
    AlertSeverity.WARNING,
    'BTCUSDT',
    'RSI above 70',
    price=45000.00
)

# Get alerts
alerts = alert_mgr.get_alerts(symbol='BTCUSDT', limit=10)

# Get critical alerts
critical = alert_mgr.get_critical_alerts()

# Subscribe to alerts
alert_mgr.subscribe(AlertType.RSI_OVERBOUGHT, callback_function)
```

### IntradrDayMonitor

```python
from src.monitor import IntradrDayMonitor

monitor = IntradrDayMonitor()

# Get current state
state = monitor.get_current_state()

# Get alerts summary
summary = monitor.get_alerts_summary()

# Stop monitoring
monitor.stop()
```

## Alert Types

| Alert Type | Description | Severity |
|---|---|---|
| `PRICE_BREAKOUT` | Price breaks support/resistance | WARNING |
| `RSI_OVERBOUGHT` | RSI > 70 | WARNING |
| `RSI_OVERSOLD` | RSI < 30 | WARNING |
| `MACD_CROSSOVER` | MACD line crosses signal line | INFO |
| `BOLLINGER_BAND_TOUCH` | Price touches band | INFO |
| `LIQUIDATION_SPIKE` | High liquidation volume | CRITICAL |
| `FUNDING_RATE_EXTREME` | Unusual funding rate | WARNING |
| `VOLUME_SURGE` | Abnormal volume | INFO |

## Performance

- **Data Points Cached**: Up to 500 price points (~8 hours at 60s intervals)
- **Check Interval**: Configurable, default 60 seconds
- **Memory Usage**: ~10-15 MB typical
- **API Rate**: Respects Bybit API rate limits

## Error Handling

The monitor includes comprehensive error handling:
- Network failures are logged and recovered
- Invalid data is skipped
- Alerts are persisted even during errors
- Automatic reconnection on API failures

## Logging

Configure logging via `.env`:

```env
LOG_LEVEL=INFO       # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=monitor.log # Log file path
```

Logs include:
- Market data fetches
- Indicator calculations
- Alert generation
- API errors
- System events

## Testing

```bash
# Run with DEBUG logging
LOG_LEVEL=DEBUG python -m src.monitor

# Test specific components
python -c "from src.indicators.calculator import IndicatorCalculator; calc = IndicatorCalculator(); print(calc.sma([100, 101, 102, ...]))"
```

## Troubleshooting

### No alerts generated
- Check indicator calculations with debug logging
- Verify alert thresholds in `.env`
- Ensure sufficient price history (minimum 20 data points)

### API connection errors
- Verify internet connectivity
- Check Bybit API status
- Review API rate limits

### High memory usage
- Reduce `MAX_PRICE_HISTORY`
- Lower `ALERT_RETENTION`
- Increase `CHECK_INTERVAL`

## Dependencies

- **requests**: HTTP client for API calls
- **aiohttp**: Async HTTP support
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation
- **pytz**: Timezone handling
- **websockets**: WebSocket support (optional)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please open a GitHub issue.

## Disclaimer

This tool is for educational and informational purposes only. Trading cryptocurrencies carries risk. Use this tool at your own risk and conduct your own research before making trading decisions.

---

**Last Updated**: July 2026
**Version**: 0.1.0
