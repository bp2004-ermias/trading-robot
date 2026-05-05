from config.bot_config import (
    STARTING_CAPITAL, RISK_PER_TRADE, DAILY_LOSS_LIMIT,
    RISK_REWARD_RATIO, MAX_TRADES_PER_DAY
)
from utils.logger import log_message

class RiskManager:
    """Manages position sizing and risk"""
    
    def __init__(self, account_info):
        self.starting_capital = STARTING_CAPITAL
        self.risk_per_trade = RISK_PER_TRADE
        self.daily_loss_limit = DAILY_LOSS_LIMIT
        self.max_trades_per_day = MAX_TRADES_PER_DAY
        self.trades_today = 0
        self.daily_loss = 0
        self.daily_profit = 0
        self.account_info = account_info
    
    def calculate_position_size(self, risk_distance, current_price):
        """Calculate lot size based on 1% risk rule"""
        try:
            current_balance = self.account_info.get('balance', self.starting_capital)
            risk_amount = current_balance * self.risk_per_trade
            
            if risk_distance == 0:
                log_message("❌ Risk distance is zero, cannot calculate position size")
                return 0
            
            position_size = risk_amount / risk_distance
            
            if position_size <= 0:
                log_message("❌ Invalid position size calculated")
                return 0
            
            return round(position_size, 2)
            
        except Exception as e:
            log_message(f"❌ Error calculating position size: {str(e)}")
            return 0
    
    def can_trade_today(self):
        """Check if daily loss limit reached"""
        current_balance = self.account_info.get('balance', self.starting_capital)
        max_daily_loss = current_balance * self.daily_loss_limit
        
        if self.daily_loss >= max_daily_loss:
            log_message(f"⛔ Daily loss limit reached: {self.daily_loss} / {max_daily_loss}")
            return False
        
        if self.trades_today >= self.max_trades_per_day:
            log_message(f"⛔ Max trades per day reached: {self.trades_today} / {self.max_trades_per_day}")
            return False
        
        return True
    
    def validate_trade(self, trade_signal):
        """Validate if trade should be placed"""
        if not self.can_trade_today():
            return False
        
        if trade_signal is None:
            return False
        
        setup = trade_signal.get('sell_setup') or trade_signal.get('buy_setup')
        if setup is None:
            return False
        
        risk = setup.get('risk_distance', 0)
        reward = setup.get('reward_distance', 0)
        
        if risk == 0 or reward == 0:
            return False
        
        rr_ratio = reward / risk
        if rr_ratio < 1.5:
            log_message(f"❌ Risk/Reward ratio too low: {rr_ratio}")
            return False
        
        return True
    
    def record_trade(self, is_win, profit_loss):
        """Record trade result"""
        self.trades_today += 1
        
        if is_win:
            self.daily_profit += profit_loss
        else:
            self.daily_loss += abs(profit_loss)
        
        log_message(f"Trade recorded: {'WIN' if is_win else 'LOSS'} | P/L: {profit_loss} | Daily: +{self.daily_profit} -{self.daily_loss}")
