from typing import Dict, Optional
from binance.client import Client
from loguru import logger

class LimitOrder:
    def __init__(self, client: Client):
        self.client = client

    def validate_inputs(self, symbol: str, quantity: float, price: float) -> bool:
        """
        Validate limit order inputs
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            quantity (float): Order quantity
            price (float): Limit price
            
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        try:
            # Check if symbol exists
            self.client.futures_exchange_info()
            
            # Check if quantity and price are positive
            if quantity <= 0:
                logger.error(f"Invalid quantity: {quantity}")
                return False
                
            if price <= 0:
                logger.error(f"Invalid price: {price}")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False

    def place_order(self, symbol: str, quantity: float, price: float, side: str, 
                   time_in_force: str = 'GTC', reduce_only: bool = False) -> Optional[Dict]:
        """
        Place a limit order
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            quantity (float): Order quantity
            price (float): Limit price
            side (str): Order side ('BUY' or 'SELL')
            time_in_force (str): Time in force ('GTC', 'IOC', 'FOK')
            reduce_only (bool): Whether to reduce position only
            
        Returns:
            dict: Order response from Binance API
        """
        if not self.validate_inputs(symbol, quantity, price):
            return None
            
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce=time_in_force,
                quantity=quantity,
                price=price,
                reduceOnly=reduce_only
            )
            
            logger.info(f"Limit order placed: {order}")
            return order
            
        except Exception as e:
            logger.error(f"Order placement error: {str(e)}")
            return None