# Architecture

## System Design

The BTC/USDT Intraday Monitor is built with a modular, event-driven architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Main Monitor                         │
│              (IntradrDayMonitor)                        │
└─────────────────────────────────────────────────────────┘
         │
         ├─ Data Fetcher (Bybit API)
         │  └─ Market Data
         │  └─ Liquidations
         │  └─ Funding Rates
         │
         ├─ Price History Manager
         │  └─ OHLCV Data
         │  └─ Rolling Buffer
         │
         ├─ Indicator Calculator
         │  ├─ SMA / EMA
         │  ├─ RSI
         │  ├─ MACD
         │  ├─ Bollinger Bands
         │  └─ ATR
         │
         ├─ Alert Rule Engine
         │  ├─ RSI Rules
         │  ├─ Band Rules
         │  └─ Liquidation Rules
         │
         └─ Alert Manager
            ├─ Alert Creation
            ├─ Alert Storage
            ├─ Subscriber Callbacks
            └─ Notification System
```

## Data Flow

```
1. Fetch Market Data (Bybit)
   ↓
2. Update Price History
   ↓
3. Calculate Indicators
   ↓
4. Evaluate Rules
   ↓
5. Generate Alerts
   ↓
6. Notify Subscribers
   ↓
7. Store for Analysis
```

## Component Details

### 1. IntradrDayMonitor (Main Orchestrator)

**Responsibilities**:
- Coordinate all components
- Manage monitoring loop
- Track application state
- Expose public API

**Key Methods**:
```python
async def start()           # Start monitoring loop
async def run_check()       # Single check cycle
def get_current_state()     # Fetch current state
def get_alerts_summary()    # Alert statistics
```

### 2. BybitFetcher (Data Integration)

**Responsibilities**:
- Fetch market data from Bybit
- Handle API errors and retries
- Parse responses
- Manage rate limits

**Methods**:
```python
def get_tickers()           # Price data
def get_funding_rate()      # Funding rates
def get_open_interest()     # Open interest
def get_liquidation_data()  # Liquidations
```

### 3. IndicatorCalculator (Analysis)

**Responsibilities**:
- Calculate technical indicators
- Handle insufficient data
- Optimize performance
- Return results in standard format

**Methods**:
```python
static def sma()            # Simple Moving Average
static def ema()            # Exponential Moving Average
static def rsi()            # Relative Strength Index
static def macd()           # MACD
static def bollinger_bands()# Bollinger Bands
static def atr()            # Average True Range
```

### 4. AlertRuleEngine (Rule Evaluation)

**Responsibilities**:
- Check trading conditions
- Compare against thresholds
- Trigger appropriate alerts
- Classify by severity

**Methods**:
```python
def check_rsi_levels()              # RSI checks
def check_bollinger_bands()         # Band checks
def check_liquidation_spike()       # Liquidation checks
```

### 5. AlertManager (Alert Handling)

**Responsibilities**:
- Create and store alerts
- Manage alert lifecycle
- Notify subscribers
- Filter and retrieve alerts

**Methods**:
```python
def create_alert()          # Create new alert
def get_alerts()            # Retrieve with filters
def subscribe()             # Subscribe to alerts
def acknowledge_alert()     # Mark as acknowledged
```

## Configuration Layer

**config.py** provides centralized configuration:
- API settings
- Indicator parameters
- Alert thresholds
- Logging configuration
- Notification settings

## State Management

### Price History
```python
price_history = {
    'timestamps': [...],
    'opens': [...],
    'highs': [...],
    'lows': [...],
    'closes': [...],
    'volumes': [...]
}
```

Maintains rolling buffer of recent prices for indicator calculation.

### Current State
```python
current_state = {
    'market_data': {...},
    'indicators': {...},
    'timestamp': datetime
}
```

Stores latest calculated values.

## Alert System

### Alert Structure
```python
class Alert:
    alert_type: AlertType           # Type of alert
    severity: AlertSeverity         # INFO, WARNING, CRITICAL
    symbol: str                     # Trading symbol
    message: str                    # Human-readable message
    price: float                    # Price at alert time
    timestamp: datetime             # Alert timestamp
    metadata: dict                  # Additional context
    acknowledged: bool              # Acknowledgement status
```

### Alert Types
```python
class AlertType(Enum):
    PRICE_BREAKOUT
    RSI_OVERBOUGHT
    RSI_OVERSOLD
    MACD_CROSSOVER
    BOLLINGER_BAND_TOUCH
    LIQUIDATION_SPIKE
    FUNDING_RATE_EXTREME
    VOLUME_SURGE
```

## Error Handling

### API Errors
```python
try:
    data = fetcher.get_tickers(symbol)
except APIError:
    logger.error("API error")
    return None  # Skip this check
```

### Data Validation
```python
if not market_data:
    logger.warning("Invalid data")
    return
```

### Graceful Degradation
- Insufficient data: Return None for indicators
- API unavailable: Log and retry next cycle
- Invalid configuration: Use defaults

## Performance Optimization

### Memory Management
- Rolling buffer limits history size
- Alert pruning removes old entries
- Efficient data structures

### Computation Efficiency
- Vectorized calculations where possible
- Caching of common values
- Lazy indicator calculation

### API Optimization
- Single request per check cycle
- Response caching
- Batch operations

## Scalability Considerations

### Current Design
- Single symbol monitoring
- In-memory storage
- Synchronous API calls

### Future Enhancements
- Multi-symbol support
- Database persistence
- Async API calls
- WebSocket support
- Distributed architecture

## Testing Strategy

### Unit Tests
- Indicator calculations
- Alert creation
- Rule evaluation

### Integration Tests
- Full monitoring cycle
- API integration
- Alert notifications

### Performance Tests
- Memory usage
- CPU usage
- API response times

---

For implementation details, refer to specific module documentation.
