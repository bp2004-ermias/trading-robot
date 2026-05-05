#!/usr/bin/env python3
"""
Volatility 10 Trading Robot
Liquidity Grab + Price Action Strategy
For Deriv via MT5
"""

import sys
from trading.bot import VolatilityBot
from utils.logger import log_message

def main():
    """Main entry point"""
    
    log_message("\n" + "="*60)
    log_message("🤖 VOLATILITY 10 TRADING BOT")
    log_message("Strategy: Liquidity Grab + Price Action")
    log_message("Platform: Deriv (MT5)")
    log_message("="*60 + "\n")
    
    try:
        bot = VolatilityBot()
        bot.run(interval=300)
        
    except KeyboardInterrupt:
        log_message("\n⛔ Bot interrupted by user")
        sys.exit(0)
    except Exception as e:
        log_message(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
