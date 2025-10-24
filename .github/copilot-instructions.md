# TradeSignals Copilot Instructions

## Project Overview
This is a real-time cryptocurrency alert system that monitors Solana (SOL) price movements against a 15-minute EMA50 indicator. The system triggers alerts when the gap between current price and EMA50 falls within a configurable threshold.

### Core Architecture

### Single-Class Design
- `SOLAlertSystem` in `app.py` handles all functionality: CCXT integration, EMA calculations, alerting, and monitoring loop
- Uses `deque(maxlen=50)` for efficient rolling window of 15-minute price history
- Employs custom EMA calculation with multiplier approach: `((price - ema[-1]) * multiplier) + ema[-1]`

### Data Flow Pattern
1. **Initialization**: Fetch 50 historical 15-min candles to bootstrap EMA calculation
2. **Monitoring Loop**: Check current price every 30 seconds, update history every 15 minutes
3. **Alert Logic**: Compare `abs(current_price - ema50) <= threshold` with cooldown protection

## Key Implementation Details

### API Integration
- Uses CCXT library with Binance exchange (`ccxt.binance()`)
- Leverages `fetch_ticker()` for current price and `fetch_ohlcv()` for historical data
- CCXT handles exchange-specific details, rate limiting, and error handling automatically
- Symbol format: `SOL/USDT` (CCXT standard format, no manual conversion needed)

### Time Management
- **Price Updates**: Every 30 seconds via `get_current_price()`
- **History Updates**: Every 15 minutes (900 seconds) via `update_price_history()`
- **Alert Cooldown**: Configurable (default 300 seconds) to prevent spam

### Configuration Approach
- Runtime configuration via direct property assignment in `main()` function
- `config.json` exists but is NOT currently used by the application code
- To modify behavior, edit parameters in `main()` or class `__init__`

## Development Workflows

### Running the System
```bash
python app.py
```
No additional setup required beyond `pip install -r requirements.txt`

### Testing Changes
- No automated tests exist - verify changes by running the monitor and checking console output
- Monitor initialization logs to ensure price history loads correctly
- Test alert conditions by temporarily lowering `alert_threshold` value

### Extending Notifications
The `send_alert()` method is designed for extension. Add new notification channels by implementing additional calls after the console print:

```python
def send_alert(self, current_price, ema50, gap):
    # Existing console output...
    # Add your notification method here
```

## Project-Specific Patterns

### Error Handling Strategy
- CCXT network and exchange errors trigger automatic retries with 30-second delays
- Failed API calls return `None`, system continues with cached data
- Global exception handler restarts monitoring loop after 60 seconds

### Price Data Management
- Uses completed candles only (second-to-last from API response) to avoid incomplete data
- Deduplication check: `latest_close != self.price_history[-1]` prevents duplicate entries
- EMA requires minimum 50 data points before alerts can trigger

### Configuration Gotcha
The system has dual configuration - `config.json` exists but is unused. Active configuration happens in `main()` function. When adding new features, decide whether to extend the runtime configuration pattern or implement JSON config loading.