# Technical Indicators Reference

## Overview

This document explains the technical indicators implemented in the BTC/USDT Intraday Monitor.

## Indicators

### Simple Moving Average (SMA)

**Purpose**: Smooth price data and identify trends

**Formula**:
```
SMA = (P1 + P2 + ... + Pn) / n
```

**Default Period**: 20

**Interpretation**:
- Price above SMA: Uptrend
- Price below SMA: Downtrend
- SMA slope: Trend strength

**Example**:
```python
from src.indicators.calculator import IndicatorCalculator

calc = IndicatorCalculator()
prices = [45000, 45100, 45200, ...]
sma = calc.sma(prices, period=20)
```

---

### Exponential Moving Average (EMA)

**Purpose**: Responsive moving average that gives more weight to recent prices

**Formula**:
```
Multiplier = 2 / (n + 1)
EMA = Price * Multiplier + Previous_EMA * (1 - Multiplier)
```

**Default Period**: 20

**Advantages over SMA**:
- Responds faster to price changes
- Better for identifying trend reversals
- Reduces lag

---

### Relative Strength Index (RSI)

**Purpose**: Measure momentum and identify overbought/oversold conditions

**Formula**:
```
RS = Average_Gain / Average_Loss
RSI = 100 - (100 / (1 + RS))
```

**Default Period**: 14

**Interpretation**:
- RSI > 70: Overbought (potential sell signal)
- RSI < 30: Oversold (potential buy signal)
- RSI = 50: Neutral

**Alert Thresholds** (configurable):
- Overbought: 70 (default)
- Oversold: 30 (default)

**Example**:
```python
rsi = calc.rsi(prices, period=14)
if rsi > 70:
    print("Overbought condition")
```

---

### MACD (Moving Average Convergence Divergence)

**Purpose**: Identify trend changes and momentum

**Components**:
- **MACD Line**: 12-period EMA - 26-period EMA
- **Signal Line**: 9-period EMA of MACD line
- **Histogram**: MACD Line - Signal Line

**Signals**:
- MACD crosses above signal line: Bullish
- MACD crosses below signal line: Bearish
- Positive histogram: Upward momentum
- Negative histogram: Downward momentum

**Example**:
```python
macd_line, signal_line, histogram = calc.macd(prices)
if macd_line[-1] > signal_line[-1]:
    print("Bullish signal")
```

---

### Bollinger Bands

**Purpose**: Identify volatility and potential reversal points

**Formula**:
```
Middle Band = SMA(n)
Upper Band = SMA(n) + (StdDev * 2)
Lower Band = SMA(n) - (StdDev * 2)
```

**Default Period**: 20
**Default Std Dev**: 2.0

**Interpretation**:
- Price touches upper band: Potentially overbought
- Price touches lower band: Potentially oversold
- Band width: Volatility measure
- Narrow bands: Low volatility
- Wide bands: High volatility

**Example**:
```python
upper, middle, lower = calc.bollinger_bands(prices, period=20, std_dev=2.0)

if price > upper:
    print("Price at upper band")
```

---

### Average True Range (ATR)

**Purpose**: Measure volatility

**True Range Formula**:
```
TR = max(
    High - Low,
    |High - Previous_Close|,
    |Low - Previous_Close|
)

ATR = Average of TR over n periods
```

**Default Period**: 14

**Interpretation**:
- Higher ATR: Higher volatility
- Lower ATR: Lower volatility
- Useful for setting stop losses and position sizes

**Example**:
```python
atr = calc.atr(highs, lows, closes, period=14)
stop_loss = current_price - (atr[-1] * 2)  # 2x ATR below price
```

---

## Alert Generation Rules

### RSI Alerts
```
IF RSI > 70: Generate RSI_OVERBOUGHT alert
IF RSI < 30: Generate RSI_OVERSOLD alert
```

### Bollinger Band Alerts
```
IF Price >= Upper Band: Generate BOLLINGER_BAND_TOUCH alert
IF Price <= Lower Band: Generate BOLLINGER_BAND_TOUCH alert
```

### Liquidation Alerts
```
IF Total Liquidation Volume > 1,000,000 USDT:
    IF Volume > 2,000,000: CRITICAL severity
    ELSE: WARNING severity
```

---

## Configuration Best Practices

### Short-term Trading (5-30 minutes)
```env
SMA_PERIOD=12
RSI_PERIOD=14
BOLLINGER_PERIOD=12
CHECK_INTERVAL=300  # 5 minutes
```

### Medium-term Trading (1-4 hours)
```env
SMA_PERIOD=20
RSI_PERIOD=14
BOLLINGER_PERIOD=20
CHECK_INTERVAL=600  # 10 minutes
```

### Long-term Trading (Daily+)
```env
SMA_PERIOD=50
RSI_PERIOD=21
BOLLINGER_PERIOD=20
CHECK_INTERVAL=3600  # 1 hour
```

---

## Performance Considerations

| Indicator | Time Complexity | Space | Period ||
|---|---|---|---|
| SMA | O(n) | O(1) | 20 |
| EMA | O(n) | O(1) | 20 |
| RSI | O(n) | O(1) | 14 |
| MACD | O(n) | O(n) | 26+ |
| Bollinger | O(n) | O(1) | 20 |
| ATR | O(n) | O(1) | 14 |

---

## Common Combinations

### Trend Confirmation (SMA + EMA)
```
Bullish: Price > EMA > SMA
Bearish: Price < EMA < SMA
```

### Momentum + Trend (MACD + RSI)
```
Strong Buy: MACD bullish crossover + RSI < 50
Strong Sell: MACD bearish crossover + RSI > 50
```

### Volatility + Momentum (ATR + RSI)
```
High Risk Setup: High ATR + RSI > 70
Low Risk Setup: Low ATR + RSI near 50
```

---

## References

- SMA: https://en.wikipedia.org/wiki/Moving_average
- RSI: https://en.wikipedia.org/wiki/Relative_strength_index
- MACD: https://www.investopedia.com/terms/m/macd.asp
- Bollinger Bands: https://en.wikipedia.org/wiki/Bollinger_Bands
- ATR: https://www.investopedia.com/terms/a/atr.asp
