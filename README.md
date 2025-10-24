# SOL Crypto Alert System

A real-time cryptocurrency alert system that monitors Solana (SOL) price movements and triggers alerts when the gap between the current price and the 15-minute EMA50 reaches a specified threshold.

## Features

- ✅ Real-time SOL price monitoring via Binance API
- ✅ 15-minute EMA50 calculation and tracking
- ✅ Customizable gap threshold alerts (default: $0.01)
- ✅ Alert cooldown to prevent spam notifications
- ✅ Continuous monitoring with error handling
- ✅ Historical price data initialization
- ✅ Configurable parameters

## Requirements

- Python 3.8+
- Internet connection for API access
- Required Python packages (see `requirements.txt`)

## Installation

1. **Clone or download the repository:**
   ```bash
   git clone <repository-url>
   cd TradeSignals
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

Run the alert system with default settings:
```bash
python app.py
```

### Configuration

You can customize the alert system by modifying the parameters in `app.py`:

```python
# In the main() function
alert_system.alert_threshold = 0.01  # Gap threshold in USD
alert_system.alert_cooldown = 300    # 5 minutes between alerts
```

### Default Settings

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `alert_threshold` | $0.01 | Minimum gap between current price and EMA50 to trigger alert |
| `alert_cooldown` | 300 seconds | Time between alerts to prevent spam |
| `check_interval` | 30 seconds | How often to check current price |
| `ema_period` | 50 | EMA period for calculation |
| `timeframe` | 15 minutes | Timeframe for EMA calculation |

## How It Works

1. **Initialization**: The system fetches the last 50 completed 15-minute candles from Binance to calculate the initial EMA50.

2. **Monitoring Loop**: 
   - Fetches current SOL price every 30 seconds
   - Updates 15-minute price history every 15 minutes
   - Calculates EMA50 using the historical data
   - Compares current price with EMA50

3. **Alert Trigger**: When the absolute gap between current price and EMA50 is ≤ $0.01:
   - Displays alert message with timestamp, prices, and gap
   - Implements cooldown period to prevent spam

## Output Example

```
Starting SOL Alert System...
Monitoring for gap <= $0.01 between current price and 15m EMA50
------------------------------------------------------------
Initializing price history...
Loaded 50 historical 15-min candles
[14:30:25] Price: $158.45 | EMA50: $158.52 | Gap: $0.07
[14:31:00] Price: $158.44 | EMA50: $158.52 | Gap: $0.08
[14:31:30] Price: $158.51 | EMA50: $158.52 | Gap: $0.01

==================================================
🚨 SOL ALERT TRIGGERED! 🚨
Time: 2025-10-24 14:31:30
Current Price: $158.51
EMA50 (15m): $158.52
Gap: $0.01
Threshold: $0.01
==================================================
```

## File Structure

```
TradeSignals/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── config.json        # Configuration settings (optional)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Customization

### Modifying Alert Threshold

To change the gap threshold that triggers alerts:

```python
# In app.py main() function
alert_system.alert_threshold = 0.005  # $0.005 instead of $0.01
```

### Adding Custom Notifications

You can extend the `send_alert()` method to add additional notification methods:

```python
def send_alert(self, current_price, ema50, gap):
    # Existing console alert code...
    
    # Add email notification
    # send_email_alert(current_price, ema50, gap)
    
    # Add Discord/Slack notification
    # send_discord_alert(current_price, ema50, gap)
    
    # Add desktop notification
    # send_desktop_notification(current_price, ema50, gap)
```

### Monitoring Different Cryptocurrencies

To monitor a different cryptocurrency, modify the symbol in the `__init__` method:

```python
def __init__(self):
    self.symbol = "BTC/USDT"  # Change from SOL/USDT to BTC/USDT
    # Update API calls to use "BTCUSDT" instead of "SOLUSDT"
```

## Troubleshooting

### Common Issues

1. **Network Connection Errors**:
   - Ensure you have a stable internet connection
   - Check if Binance API is accessible from your location
   - The system will retry automatically after errors

2. **Price Data Not Loading**:
   - Verify the symbol "SOLUSDT" is correct
   - Check Binance API status at https://status.binance.com/

3. **EMA Calculation Issues**:
   - The system needs at least 50 data points for EMA50
   - Wait for initialization to complete before alerts can trigger

### Error Messages

- `"Not enough data for EMA50 calculation"`: System is still initializing
- `"Failed to fetch current price"`: Network or API issue, will retry automatically
- `"Error updating price history"`: Temporary API issue, will continue with cached data

## API Rate Limits

The system is designed to respect Binance API rate limits:
- Current price: Fetched every 30 seconds
- Historical data: Updated every 15 minutes
- No API key required for public endpoints

## Security Notes

- This system uses public Binance API endpoints (no authentication required)
- No trading functionality - monitoring only
- No sensitive data is stored locally
- API calls are read-only

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This tool is for informational purposes only. It is not financial advice. Cryptocurrency trading involves substantial risk of loss. Always do your own research before making any trading decisions.

---

**Need help?** Check the troubleshooting section above or review the code comments in `app.py` for more details.