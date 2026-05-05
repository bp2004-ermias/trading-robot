import MetaTrader5 as mt5
import time
from config.bot_config import MT5_ACCOUNT, MT5_PASSWORD, MT5_SERVER
from utils.logger import log_message

class MT5Connector:
    """Handles MT5 connection and operations"""
    
    def __init__(self):
        self.connected = False
        self.account = MT5_ACCOUNT
        self.password = MT5_PASSWORD
        self.server = MT5_SERVER
    
    def connect(self):
        """Connect to MT5"""
        try:
            if not mt5.initialize():
                raise Exception(f"MT5 initialization failed: {mt5.last_error()}")
            
            authorized = mt5.login(
                login=self.account,
                password=self.password,
                server=self.server
            )
            
            if not authorized:
                raise Exception(f"MT5 login failed: {mt5.last_error()}")
            
            self.connected = True
            log_message(f"✅ Connected to MT5 - Account: {self.account}")
            return True
            
        except Exception as e:
            log_message(f"❌ MT5 Connection Error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            log_message("MT5 disconnected")
    
    def get_candles(self, symbol, timeframe, num_candles=100):
        """Fetch candlestick data"""
        try:
            tf_map = {5: mt5.TIMEFRAME_M5, 15: mt5.TIMEFRAME_M15, 30: mt5.TIMEFRAME_M30, 60: mt5.TIMEFRAME_H1}
            mt5_timeframe = tf_map.get(timeframe, mt5.TIMEFRAME_M5)
            
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, num_candles)
            
            if rates is None:
                log_message(f"❌ Failed to fetch candles for {symbol}")
                return None
            
            return rates
            
        except Exception as e:
            log_message(f"❌ Error fetching candles: {str(e)}")
            return None
    
    def get_account_info(self):
        """Get account information"""
        try:
            account_info = mt5.account_info()
            if account_info:
                return {
                    'balance': account_info.balance,
                    'equity': account_info.equity,
                    'margin': account_info.margin,
                    'margin_free': account_info.margin_free,
                    'leverage': account_info.leverage
                }
            return None
        except Exception as e:
            log_message(f"❌ Error getting account info: {str(e)}")
            return None
