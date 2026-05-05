import time
from datetime import datetime
from core.mt5_connector import MT5Connector
from core.market_data import MarketData
from core.strategy import PriceActionStrategy
from core.risk_manager import RiskManager
from config.bot_config import ASSET_SYMBOL, MAX_TRADES_PER_DAY, DEBUG_MODE
from utils.logger import log_message, log_trade

class VolatilityBot:
    """Main trading bot"""
    
    def __init__(self):
        self.mt5 = MT5Connector()
        self.market_data = None
        self.strategy = None
        self.risk_manager = None
        self.running = False
        self.last_signal_time = None
        self.active_trades = []
    
    def initialize(self):
        """Initialize bot components"""
        try:
            if not self.mt5.connect():
                log_message("❌ Failed to connect to MT5")
                return False
            
            self.market_data = MarketData(self.mt5)
            self.strategy = PriceActionStrategy(self.market_data, ASSET_SYMBOL)
            
            account_info = self.mt5.get_account_info()
            if account_info is None:
                log_message("❌ Failed to get account info")
                return False
            
            self.risk_manager = RiskManager(account_info)
            
            log_message("✅ Bot initialized successfully")
            log_message(f"Account Balance: ${account_info['balance']}")
            return True
            
        except Exception as e:
            log_message(f"❌ Initialization error: {str(e)}")
            return False
    
    def check_signal(self):
        """Check for trading signals"""
        try:
            signal = self.strategy.get_trade_signal()
            
            if signal is None:
                if DEBUG_MODE:
                    log_message("No signal generated")
                return None
            
            if DEBUG_MODE:
                log_message(f"Signal detected: Structure={signal['structure']['trend']}")
            
            return signal
            
        except Exception as e:
            log_message(f"❌ Error checking signal: {str(e)}")
            return None
    
    def execute_trade(self, signal):
        """Execute trade based on signal"""
        try:
            if not self.risk_manager.validate_trade(signal):
                if DEBUG_MODE:
                    log_message("Trade validation failed")
                return False
            
            sell_setup = signal.get('sell_setup')
            buy_setup = signal.get('buy_setup')
            
            setup = sell_setup if sell_setup else buy_setup
            
            if setup is None:
                return False
            
            position_size = self.risk_manager.calculate_position_size(
                setup['risk_distance'],
                setup['entry_price']
            )
            
            if position_size <= 0:
                log_message("❌ Invalid position size")
                return False
            
            log_message(f"📋 Placing {setup['type']} order: Size={position_size}, Entry={setup['entry_price']:.2f}, SL={setup['stop_loss']:.2f}, TP={setup['take_profit']:.2f}")
            
            trade_info = {
                'timestamp': datetime.now(),
                'type': setup['type'],
                'entry_price': setup['entry_price'],
                'stop_loss': setup['stop_loss'],
                'take_profit': setup['take_profit'],
                'position_size': position_size,
                'risk_distance': setup['risk_distance'],
                'reward_distance': setup['reward_distance'],
                'signal': setup.get('signal', 'Price Action')
            }
            
            log_trade(trade_info)
            
            self.active_trades.append(trade_info)
            self.last_signal_time = datetime.now()
            
            return True
            
        except Exception as e:
            log_message(f"❌ Error executing trade: {str(e)}")
            return False
    
    def run(self, interval=300):
        """Main bot loop (interval in seconds)"""
        try:
            if not self.initialize():
                return
            
            self.running = True
            log_message(f"🤖 Bot started | Checking signals every {interval} seconds")
            
            while self.running:
                try:
                    signal = self.check_signal()
                    
                    if signal:
                        self.execute_trade(signal)
                    
                    time.sleep(interval)
                    
                except KeyboardInterrupt:
                    log_message("\n⛔ Bot stopped by user")
                    self.running = False
                except Exception as e:
                    log_message(f"❌ Error in bot loop: {str(e)}")
                    time.sleep(interval)
            
        except Exception as e:
            log_message(f"❌ Fatal error: {str(e)}")
        finally:
            self.mt5.disconnect()
            log_message("Bot shutdown complete")
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        log_message("Bot stopping...")
