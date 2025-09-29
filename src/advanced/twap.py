from typing import Dict, List, Optional
from binance.client import Client
from loguru import logger
import time

class TWAPOrder:
    def __init__(self, client: Client):
        self.client = client

    def validate_inputs(self, symbol: str, total_quantity: float, num_chunks: int, 
                       interval_seconds: int) -> bool:
        """
        Validate TWAP order inputs
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            total_quantity (float): Total order quantity
            num_chunks (int): Number of chunks to split the order into
            interval_seconds (int): Time interval between chunks in seconds
            
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        try:
            # Check if symbol exists
            self.client.futures_exchange_info()
            
            # Validate numeric inputs
            if total_quantity <= 0:
                logger.error(f"Invalid total quantity: {total_quantity}")
                return False
                
            if num_chunks <= 0:
                logger.error(f"Invalid number of chunks: {num_chunks}")
                return False
                
            if interval_seconds <= 0:
                logger.error(f"Invalid interval: {interval_seconds}")
                return False
                
            # Check if chunk size is valid
            chunk_size = total_quantity / num_chunks
            if chunk_size < 0.001:  # Minimum order size for most pairs
                logger.error(f"Chunk size too small: {chunk_size}")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False

    def execute_twap(self, symbol: str, total_quantity: float, num_chunks: int,
                    interval_seconds: int, side: str) -> Optional[List[Dict]]:
        """
        Execute a TWAP (Time-Weighted Average Price) order
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            total_quantity (float): Total order quantity
            num_chunks (int): Number of chunks to split the order into
            interval_seconds (int): Time interval between chunks in seconds
            side (str): Order side ('BUY' or 'SELL')
            
        Returns:
            list: List of order responses from Binance API
        """
        if not self.validate_inputs(symbol, total_quantity, num_chunks, interval_seconds):
            return None
            
        try:
            chunk_size = total_quantity / num_chunks
            orders = []
            
            for i in range(num_chunks):
                # Place market order for the chunk
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=chunk_size
                )
                
                orders.append(order)
                logger.info(f"TWAP chunk {i+1}/{num_chunks} executed: {order}")
                
                # Wait for the interval if not the last chunk
                if i < num_chunks - 1:
                    time.sleep(interval_seconds)
            
            return orders
            
        except Exception as e:
            logger.error(f"TWAP execution error: {str(e)}")
            return None