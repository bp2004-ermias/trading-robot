import csv
from datetime import datetime
from config.bot_config import LOG_FILE, LOG_TRADES

def log_message(message):
    """Log message to console with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def log_trade(trade_info):
    """Log trade to CSV file"""
    if not LOG_TRADES:
        return
    
    try:
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            
            if f.tell() == 0:
                writer.writerow([
                    'Timestamp', 'Type', 'Entry Price', 'Stop Loss', 'Take Profit',
                    'Position Size', 'Risk Distance', 'Reward Distance', 'Signal'
                ])
            
            writer.writerow([
                trade_info['timestamp'],
                trade_info['type'],
                trade_info['entry_price'],
                trade_info['stop_loss'],
                trade_info['take_profit'],
                trade_info['position_size'],
                trade_info['risk_distance'],
                trade_info['reward_distance'],
                trade_info['signal']
            ])
        
        log_message(f"✅ Trade logged to {LOG_FILE}")
    except Exception as e:
        log_message(f"❌ Error logging trade: {str(e)}")
