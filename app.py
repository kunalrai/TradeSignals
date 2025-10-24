import ccxt
import time
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from collections import deque
import json
import sys

class SOLAlertSystem:
    def __init__(self):
        self.symbol = "SOL/USDT"
        self.exchange = ccxt.binance()  # Initialize CCXT Binance exchange
        self.price_history = deque(maxlen=50)  # Store last 50 15-min candles for EMA
        self.ema_period = 50
        self.alert_threshold = 0.01
        self.last_alert_time = None
        self.alert_cooldown = 300  # 5 minutes cooldown between alerts
        
    def get_current_price(self):
        """Fetch current SOL price using CCXT"""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return float(ticker['last'])
        except ccxt.NetworkError as e:
            print(f"Network error fetching current price: {e}")
            return None
        except ccxt.ExchangeError as e:
            print(f"Exchange error fetching current price: {e}")
            return None
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None
    
    def get_15min_klines(self, limit=50):
        """Fetch 15-minute OHLCV data using CCXT"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '15m', limit=limit)
            # Extract closing prices (close is at index 4 in OHLCV)
            closes = [candle[4] for candle in ohlcv]
            return closes
        except ccxt.NetworkError as e:
            print(f"Network error fetching OHLCV data: {e}")
            return None
        except ccxt.ExchangeError as e:
            print(f"Exchange error fetching OHLCV data: {e}")
            return None
        except Exception as e:
            print(f"Error fetching OHLCV data: {e}")
            return None
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average using efficient method"""
        if len(prices) < period:
            return None
        
        # Start with simple moving average for first value
        ema = [sum(prices[:period]) / period]
        multiplier = 2 / (period + 1)
        
        # Calculate EMA for remaining values
        for price in prices[period:]:
            ema.append(((price - ema[-1]) * multiplier) + ema[-1])
        
        return ema[-1]  # Return the latest EMA value
    
    def initialize_price_history(self):
        """Initialize price history with recent 15-min klines"""
        print("Initializing price history...")
        closes = self.get_15min_klines(50)
        if closes:
            self.price_history.extend(closes)
            print(f"Loaded {len(closes)} historical 15-min candles")
            return True
        return False
    
    def send_alert(self, current_price, ema50, gap):
        """Send alert notification"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"""
🚨 SOL ALERT TRIGGERED! 🚨
Time: {timestamp}
Current Price: ${current_price:.4f}
EMA50 (15m): ${ema50:.4f}
Gap: ${gap:.4f}
Threshold: ${self.alert_threshold}
        """
        
        print("=" * 50)
        print(alert_message)
        print("=" * 50)
        
        # Here you can add additional notification methods:
        # - Email notifications
        # - Discord/Telegram bot
        # - SMS alerts
        # - Desktop notifications
        
        self.last_alert_time = time.time()
    
    def should_send_alert(self):
        """Check if enough time has passed since last alert"""
        if self.last_alert_time is None:
            return True
        return time.time() - self.last_alert_time > self.alert_cooldown
    
    def check_alert_condition(self, current_price):
        """Check if alert condition is met"""
        if len(self.price_history) < self.ema_period:
            print(f"Not enough data for EMA50 calculation. Have {len(self.price_history)}, need {self.ema_period}")
            return False
        
        # Calculate EMA50
        ema50 = self.calculate_ema(list(self.price_history), self.ema_period)
        
        if ema50 is None:
            return False
        
        # Calculate gap
        gap = abs(current_price - ema50)
        
        # Log current status
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Price: ${current_price:.4f} | EMA50: ${ema50:.4f} | Gap: ${gap:.4f}")
        
        # Check if alert condition is met
        if gap <= self.alert_threshold and self.should_send_alert():
            self.send_alert(current_price, ema50, gap)
            return True
        
        return False
    
    def update_price_history(self):
        """Update price history with latest 15-min candle close"""
        try:
            # Get the latest 2 completed 15-min candles
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '15m', limit=2)
            if ohlcv and len(ohlcv) >= 2:
                latest_close = ohlcv[-2][4]  # Use the second-to-last (completed candle)
                
                # Only add if it's different from the last price in history
                if not self.price_history or latest_close != self.price_history[-1]:
                    self.price_history.append(latest_close)
                    print(f"Updated price history with new 15m close: ${latest_close:.4f}")
                    return True
        except Exception as e:
            print(f"Error updating price history: {e}")
        
        return False
    
    def run_monitor(self):
        """Main monitoring loop"""
        print("Starting SOL Alert System...")
        print(f"Monitoring for gap <= ${self.alert_threshold} between current price and 15m EMA50")
        print("-" * 60)
        
        # Initialize price history
        if not self.initialize_price_history():
            print("Failed to initialize price history. Exiting.")
            return
        
        last_history_update = time.time()
        history_update_interval = 900  # Update every 15 minutes (900 seconds)
        
        try:
            while True:
                # Get current price
                current_price = self.get_current_price()
                
                if current_price is None:
                    print("Failed to fetch current price. Retrying in 30 seconds...")
                    time.sleep(30)
                    continue
                
                # Update price history every 15 minutes
                current_time = time.time()
                if current_time - last_history_update >= history_update_interval:
                    self.update_price_history()
                    last_history_update = current_time
                
                # Check alert condition
                self.check_alert_condition(current_price)
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\nStopping SOL Alert System...")
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Restarting in 60 seconds...")
            time.sleep(60)

def main():
    """Main function to run the alert system"""
    alert_system = SOLAlertSystem()
    
    # You can customize these parameters
    alert_system.alert_threshold = 0.01  # Gap threshold in USD
    alert_system.alert_cooldown = 300    # 5 minutes between alerts (changed back to 300)
    
    # Start monitoring
    alert_system.run_monitor()

if __name__ == "__main__":
    main()
