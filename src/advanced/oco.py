from typing import Dict, Optional, Tuple
from binance.client import Client
from loguru import logger

class OCOOrder:
    def __init__(self, client: Client):
        self.client = client

    def validate_inputs(self, symbol: str, quantity: float, price: float, 
                       stop_price: float, stop_limit_price: float) -> bool:
        """
        Validate OCO order inputs
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            quantity (float): Order quantity
            price (float): Limit price for take profit
            stop_price (float): Stop trigger price
            stop_limit_price (float): Limit price for stop loss
            
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        try:
            # Check if symbol exists
            self.client.futures_exchange_info()
            
            # Validate numeric inputs
            if any(x <= 0 for x in [quantity, price, stop_price, stop_limit_price]):
                logger.error("All numeric inputs must be positive")
                return False
                
            # Validate price relationships
            if price <= stop_price:
                logger.error("Take profit price must be higher than stop price for long positions")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False

    def place_order(self, symbol: str, quantity: float, price: float, 
                   stop_price: float, stop_limit_price: float, 
                   side: str = 'BUY') -> Optional[Tuple[Dict, Dict]]:
        """
        Place an OCO (One-Cancels-the-Other) order
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            quantity (float): Order quantity
            price (float): Limit price for take profit
            stop_price (float): Stop trigger price
            stop_limit_price (float): Limit price for stop loss
            side (str): Order side ('BUY' or 'SELL')
            
        Returns:
            tuple: (Take profit order response, Stop loss order response)
        """
        if not self.validate_inputs(symbol, quantity, price, stop_price, stop_limit_price):
            return None
            
        try:
            # Place take profit limit order
            take_profit = self.client.futures_create_order(
                symbol=symbol,
                side='SELL' if side == 'BUY' else 'BUY',
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                reduceOnly=True
            )
            
            # Place stop loss order
            stop_loss = self.client.futures_create_order(
                symbol=symbol,
                side='SELL' if side == 'BUY' else 'BUY',
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=stop_limit_price,
                stopPrice=stop_price,
                reduceOnly=True
            )
            
            logger.info(f"OCO order placed - Take profit: {take_profit}, Stop loss: {stop_loss}")
            return (take_profit, stop_loss)
            
        except Exception as e:
            logger.error(f"Order placement error: {str(e)}")
            return None