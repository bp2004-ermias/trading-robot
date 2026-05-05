import numpy as np
import pandas as pd

class Indicators:
    """Technical indicators for analysis"""
    
    @staticmethod
    def ema(data, period):
        """Calculate Exponential Moving Average"""
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def atr(df, period=14):
        """Calculate Average True Range"""
        df = df.copy()
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift()),
                abs(df['low'] - df['close'].shift())
            )
        )
        return df['tr'].rolling(window=period).mean()
    
    @staticmethod
    def is_bearish_engulfing(df):
        """Check if last candle is bearish engulfing"""
        if len(df) < 2:
            return False
        
        prev = df.iloc[-2]
        current = df.iloc[-1]
        
        is_bearish = (current['close'] < prev['open'] and 
                     current['open'] > prev['close'] and
                     current['close'] < prev['close'])
        
        return is_bearish
    
    @staticmethod
    def is_bullish_engulfing(df):
        """Check if last candle is bullish engulfing"""
        if len(df) < 2:
            return False
        
        prev = df.iloc[-2]
        current = df.iloc[-1]
        
        is_bullish = (current['close'] > prev['open'] and 
                     current['open'] < prev['close'] and
                     current['close'] > prev['close'])
        
        return is_bullish
    
    @staticmethod
    def is_rejection_wick(df, wick_size_ratio=0.6):
        """Check if candle shows rejection (large wick)"""
        if len(df) == 0:
            return False
        
        current = df.iloc[-1]
        body = abs(current['close'] - current['open'])
        total_range = current['high'] - current['low']
        
        if total_range == 0:
            return False
        
        wick_ratio = body / total_range
        return wick_ratio < wick_size_ratio
    
    @staticmethod
    def get_swing_high(df, lookback=20):
        """Get recent swing high"""
        if len(df) < lookback:
            return df['high'].max()
        return df['high'].tail(lookback).max()
    
    @staticmethod
    def get_swing_low(df, lookback=20):
        """Get recent swing low"""
        if len(df) < lookback:
            return df['low'].min()
        return df['low'].tail(lookback).min()
