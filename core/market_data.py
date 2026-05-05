import numpy as np
import pandas as pd
from core.mt5_connector import MT5Connector
from utils.logger import log_message

class MarketData:
    """Handles market data processing"""
    
    def __init__(self, mt5_connector: MT5Connector):
        self.mt5 = mt5_connector
    
    def get_candles_df(self, symbol, timeframe, num_candles=100):
        """Get candles as pandas DataFrame"""
        try:
            rates = self.mt5.get_candles(symbol, timeframe, num_candles)
            
            if rates is None or len(rates) == 0:
                log_message(f"❌ No candles fetched for {symbol}")
                return None
            
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']]
            df.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'spread', 'real_volume']
            
            return df.sort_values('time').reset_index(drop=True)
            
        except Exception as e:
            log_message(f"❌ Error processing candles: {str(e)}")
            return None
    
    def get_latest_candle(self, symbol, timeframe):
        """Get latest candle"""
        df = self.get_candles_df(symbol, timeframe, num_candles=2)
        if df is not None and len(df) > 0:
            return df.iloc[-1]
        return None
