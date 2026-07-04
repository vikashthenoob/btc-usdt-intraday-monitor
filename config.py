"""Configuration settings for the monitor."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BYBIT_BASE_URL = "https://api.bybit.com/v5"
BYBIT_TIMEOUT = int(os.getenv('BYBIT_TIMEOUT', '10'))

# Monitoring Configuration
MONITOR_SYMBOL = os.getenv('MONITOR_SYMBOL', 'BTCUSDT')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))  # seconds
MAX_PRICE_HISTORY = int(os.getenv('MAX_PRICE_HISTORY', '500'))

# Indicator Configuration
SMA_PERIOD = int(os.getenv('SMA_PERIOD', '20'))
RSI_PERIOD = int(os.getenv('RSI_PERIOD', '14'))
BOLLINGER_PERIOD = int(os.getenv('BOLLINGER_PERIOD', '20'))
BOLLINGER_STD_DEV = float(os.getenv('BOLLINGER_STD_DEV', '2.0'))

# Alert Thresholds
RSI_OVERBOUGHT = float(os.getenv('RSI_OVERBOUGHT', '70'))
RSI_OVERSOLD = float(os.getenv('RSI_OVERSOLD', '30'))
LIQUIDATION_THRESHOLD = float(os.getenv('LIQUIDATION_THRESHOLD', '1000000'))  # USDT
FUNDING_RATE_THRESHOLD = float(os.getenv('FUNDING_RATE_THRESHOLD', '0.001'))

# Alert Configuration
MAX_ALERTS = int(os.getenv('MAX_ALERTS', '1000'))
ALERT_RETENTION = int(os.getenv('ALERT_RETENTION', '500'))  # Keep last N alerts

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', 'monitor.log')

# Notification Configuration
ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'false').lower() == 'true'
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', '')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Database Configuration
USE_DATABASE = os.getenv('USE_DATABASE', 'false').lower() == 'true'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///monitor.db')
