# BTC/USDT Intraday Movement Monitor

A real-time monitoring system for Bitcoin (BTC/USDT) intraday price movements using **free online data sources**. Tracks the top 10 intraday drivers as outlined in the research document.

## Features

- **Real-time price monitoring** via CoinGecko & Binance public APIs
- **Technical indicators** (VWAP, ATR, RSI, Bollinger Bands)
- **Funding rate tracking** via Bybit/OKX public endpoints
- **Open interest metrics** from public data
- **Alert system** with configurable thresholds
- **Backtesting engine** for historical analysis

## Top 10 Intraday Drivers Monitored

1. **Order-book Liquidity Shocks** - Bid/ask spread extremes
2. **Order Flow Imbalance** - VPIN-like toxicity metrics
3. **Futures Funding Rate Extremes** - >±0.1% (8h normalized)
4. **Open Interest Jumps/Drops** - ±5% in 30m
5. **Liquidation Clusters** - >$20M in 30m
6. **Exchange Net Flows** - >20k BTC inflow in 1h
7. **Whale Transfers** - >1000 BTC transactions
8. **News/Social Spikes** - Sentiment z-score >2
9. **Cross-Market Triggers** - S&P move >1%, DXY move >1%
10. **Technical Thresholds** - VWAP breaches, RSI extremes, Bollinger breaks

## Quick Start

### Installation

```bash
git clone https://github.com/vikashthenoob/btc-usdt-intraday-monitor.git
cd btc-usdt-intraday-monitor
pip install -r requirements.txt
```

### Run Live Monitor

```bash
python main.py --config config.yaml
```

### Run Backtester

```bash
python backtest.py --symbol BTCUSDT --interval 5m --days 7
```

## Project Structure

```
.
├── main.py                    # Live monitoring entry point
├── backtest.py               # Historical backtesting engine
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── src/
│   ├── __init__.py
│   ├── data_fetchers/       # Free API integrations
│   │   ├── coingecko.py     # CoinGecko price data
│   │   ├── binance.py       # Binance spot/klines
│   │   └── bybit.py         # Bybit funding rates & OI
│   ├── indicators/          # Technical & on-chain signals
│   │   ├── technical.py     # RSI, ATR, Bollinger Bands
│   │   ├── microstructure.py # Order book analysis
│   │   └── derivatives.py   # Funding, OI, liquidations
│   └── alerts/              # Alert engine
│       └── threshold_checker.py
├── tests/
│   ├── test_indicators.py
│   └── test_fetchers.py
└── .github/
    └── workflows/
        └── test.yml         # CI/CD pipeline
```

## Data Sources (All Free)

| Data Type | Source | Endpoint |
|-----------|--------|----------|
| Price & Volume (1-5m) | CoinGecko, Binance API | Spot OHLCV |
| Funding Rates | Bybit, OKX Public API | Perpetuals |
| Open Interest | Bybit, Coinalyze | Global OI |
| Order Book Depth | Binance API | Level II data |
| Technical Analysis | Real-time ticks | Custom indicators |

## Configuration

Edit `config.yaml` to adjust:

```yaml
symbol: BTCUSDT
interval: 5m

thresholds:
  funding_rate_extreme: 0.001      # ±0.1%
  oi_change_percent: 0.05          # ±5% in 30m
  liquidation_volume_usd: 20       # >$20M
  exchange_inflow_btc: 20000       # >20k BTC in 1h
  sentiment_zscore: 2.0            # Sentiment extremes
  atr_multiplier: 1.5              # Volatility spikes
```

## Example Usage

### Get Real-time Price

```python
from src.data_fetchers.coingecko import CoinGeckoFetcher

fetcher = CoinGeckoFetcher()
price = fetcher.get_current_price('bitcoin')
print(f"BTC Price: ${price}")
```

### Analyze Funding Rates

```python
from src.data_fetchers.bybit import BybitFetcher

fetcher = BybitFetcher()
funding = fetcher.get_funding_rate('BTCUSDT')
print(f"Funding Rate: {funding}")
```

### Compute Technical Indicators

```python
from src.indicators.technical import TechnicalIndicators

prices = [100, 101, 102, 103, 104, 105]
rsi = TechnicalIndicators.rsi(prices, period=14)
bb = TechnicalIndicators.bollinger_bands(prices, period=20)
print(f"RSI: {rsi}, Bollinger: {bb}")
```

## Running Tests

```bash
pytest tests/ -v --cov=src/
```

## Thresholds (Research-based)

| Signal | Threshold | Action |
|--------|-----------|--------|
| Bid/ask spread | >2σ of hourly mean | Alert: Illiquidity |
| Funding rate | >±0.1% (8h) | Alert: Extreme leverage |
| Open Interest | ±5% in 30m | Alert: Large entry/exit |
| Liquidations | >$20M in 30m | Alert: Cascade risk |
| Exchange inflow | >20k BTC in 1h | Alert: Selling pressure |
| Social sentiment | z-score >2 | Alert: Sentiment extreme |
| Price move | >1.5×ATR | Alert: Volatility spike |

## Next Steps

- [ ] Add WebSocket support for real-time updates
- [ ] Implement ML-based signal filtering
- [ ] Add Telegram/Discord notifications
- [ ] Build web dashboard (FastAPI + React)
- [ ] Deploy to cloud (AWS/GCP)

## Disclaimer

**For educational purposes only.** Not financial advice. Do your own research before trading. Past performance does not guarantee future results.

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Please submit PRs with tests.
