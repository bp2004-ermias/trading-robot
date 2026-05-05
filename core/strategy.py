import numpy as np
from core.indicators import Indicators
from config.bot_config import (
    TIMEFRAME_STRUCTURE, TIMEFRAME_ENTRY, EMA_PERIOD, ATR_PERIOD,
    STOP_LOSS_ATR_MULTIPLIER, TAKE_PROFIT_ATR_MULTIPLIER, MIN_CANDLES_FOR_ANALYSIS
)
from utils.logger import log_message

class PriceActionStrategy:
    """Liquidity grab + price action strategy"""
    
    def __init__(self, market_data, asset_symbol):
        self.market_data = market_data
        self.asset_symbol = asset_symbol
        self.indicators = Indicators()
    
    def analyze_structure(self):
        """Analyze M30 structure for trend and key levels"""
        try:
            df_structure = self.market_data.get_candles_df(self.asset_symbol, TIMEFRAME_STRUCTURE, MIN_CANDLES_FOR_ANALYSIS)
            
            if df_structure is None or len(df_structure) < MIN_CANDLES_FOR_ANALYSIS:
                return None
            
            df_structure['ema'] = self.indicators.ema(df_structure['close'], EMA_PERIOD)
            
            current_close = df_structure['close'].iloc[-1]
            ema_value = df_structure['ema'].iloc[-1]
            
            trend = 'BULLISH' if current_close > ema_value else 'BEARISH'
            swing_high = self.indicators.get_swing_high(df_structure, lookback=10)
            swing_low = self.indicators.get_swing_low(df_structure, lookback=10)
            
            return {
                'trend': trend,
                'swing_high': swing_high,
                'swing_low': swing_low,
                'current_price': current_close,
                'ema': ema_value
            }
            
        except Exception as e:
            log_message(f"❌ Error analyzing structure: {str(e)}")
            return None
    
    def detect_sell_setup(self, df_entry):
        """Detect sell setup: liquidity grab + rejection + bearish entry"""
        try:
            if df_entry is None or len(df_entry) < 5:
                return None
            
            rejection = self.indicators.is_rejection_wick(df_entry)
            bearish_engulfing = self.indicators.is_bearish_engulfing(df_entry)
            
            if not (rejection or bearish_engulfing):
                return None
            
            df_entry['atr'] = self.indicators.atr(df_entry, ATR_PERIOD)
            atr_value = df_entry['atr'].iloc[-1]
            
            current_high = df_entry['high'].iloc[-1]
            current_low = df_entry['low'].iloc[-1]
            
            stop_loss = current_high + (atr_value * STOP_LOSS_ATR_MULTIPLIER)
            take_profit = current_low - (atr_value * TAKE_PROFIT_ATR_MULTIPLIER)
            
            return {
                'type': 'SELL',
                'entry_price': current_low,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_distance': stop_loss - current_low,
                'reward_distance': current_low - take_profit,
                'signal': 'Bearish Engulfing + Rejection' if bearish_engulfing and rejection else ('Bearish Engulfing' if bearish_engulfing else 'Rejection Wick')
            }
            
        except Exception as e:
            log_message(f"❌ Error detecting sell setup: {str(e)}")
            return None
    
    def detect_buy_setup(self, df_entry):
        """Detect buy setup: liquidity grab + rejection + bullish entry"""
        try:
            if df_entry is None or len(df_entry) < 5:
                return None
            
            rejection = self.indicators.is_rejection_wick(df_entry)
            bullish_engulfing = self.indicators.is_bullish_engulfing(df_entry)
            
            if not (rejection or bullish_engulfing):
                return None
            
            df_entry['atr'] = self.indicators.atr(df_entry, ATR_PERIOD)
            atr_value = df_entry['atr'].iloc[-1]
            
            current_high = df_entry['high'].iloc[-1]
            current_low = df_entry['low'].iloc[-1]
            
            stop_loss = current_low - (atr_value * STOP_LOSS_ATR_MULTIPLIER)
            take_profit = current_high + (atr_value * TAKE_PROFIT_ATR_MULTIPLIER)
            
            return {
                'type': 'BUY',
                'entry_price': current_high,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_distance': current_high - stop_loss,
                'reward_distance': take_profit - current_high,
                'signal': 'Bullish Engulfing + Rejection' if bullish_engulfing and rejection else ('Bullish Engulfing' if bullish_engulfing else 'Rejection Wick')
            }
            
        except Exception as e:
            log_message(f"❌ Error detecting buy setup: {str(e)}")
            return None
    
    def get_trade_signal(self):
        """Get complete trade signal with structure + entry analysis"""
        try:
            structure = self.analyze_structure()
            if structure is None:
                return None
            
            df_entry = self.market_data.get_candles_df(self.asset_symbol, TIMEFRAME_ENTRY, 30)
            if df_entry is None:
                return None
            
            sell_setup = self.detect_sell_setup(df_entry)
            buy_setup = self.detect_buy_setup(df_entry)
            
            signal = {
                'structure': structure,
                'sell_setup': sell_setup,
                'buy_setup': buy_setup,
                'timestamp': df_entry['time'].iloc[-1]
            }
            
            return signal
            
        except Exception as e:
            log_message(f"❌ Error getting trade signal: {str(e)}")
            return None
