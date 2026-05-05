import os
from dotenv import load_dotenv

load_dotenv()

# MT5 Configuration
MT5_ACCOUNT = int(os.getenv('MT5_ACCOUNT', '32208901'))
MT5_PASSWORD = os.getenv('MT5_PASSWORD')
MT5_SERVER = os.getenv('MT5_SERVER', 'Deriv-Demo')

# Bot Configuration
STARTING_CAPITAL = float(os.getenv('STARTING_CAPITAL', 40))
RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 0.01))  # 1% per trade
DAILY_LOSS_LIMIT = float(os.getenv('DAILY_LOSS_LIMIT', 0.03))  # 3% per day
MAX_TRADES_PER_DAY = 5

# Trading Parameters
ASSET_SYMBOL = 'Volatility10'  # Volatility 10 Index
TIMEFRAME_STRUCTURE = 30  # M30 for structure
TIMEFRAME_ENTRY = 5  # M5 for entry precision

# Risk Management
RISK_REWARD_RATIO = 2  # 1:2 RR (SL = 1x, TP = 2x)
STOP_LOSS_ATR_MULTIPLIER = 1.2
TAKE_PROFIT_ATR_MULTIPLIER = 2.4

# Strategy Parameters
EMA_PERIOD = 50
ATR_PERIOD = 14
MIN_CANDLES_FOR_ANALYSIS = 50

# Logging
LOG_TRADES = True
LOG_FILE = 'trade_log.csv'
DEBUG_MODE = False
