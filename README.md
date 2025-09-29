# Binance Futures Order Bot

A command-line trading bot for Binance USDT-M Futures that supports multiple order types with robust logging and validation.

## Features

### Core Orders
- Market Orders: Execute trades at the current market price
- Limit Orders: Place orders at specific price levels

### Advanced Orders
- OCO (One-Cancels-the-Other): Place simultaneous take-profit and stop-loss orders
- TWAP (Time-Weighted Average Price): Split large orders into smaller chunks over time

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Binance API credentials:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

## Usage

### Market Orders
```python
from binance.client import Client
from src.market_orders import MarketOrder

client = Client(api_key, api_secret)
market_order = MarketOrder(client)

# Place a market buy order
order = market_order.place_order(
    symbol='BTCUSDT',
    quantity=0.001,
    side='BUY'
)
```

### Limit Orders
```python
from src.limit_orders import LimitOrder

limit_order = LimitOrder(client)

# Place a limit sell order
order = limit_order.place_order(
    symbol='BTCUSDT',
    quantity=0.001,
    price=50000,
    side='SELL'
)
```

### OCO Orders
```python
from src.advanced.oco import OCOOrder

oco_order = OCOOrder(client)

# Place an OCO order
orders = oco_order.place_order(
    symbol='BTCUSDT',
    quantity=0.001,
    price=52000,  # Take profit
    stop_price=48000,  # Stop trigger
    stop_limit_price=47900  # Stop limit
)
```

### TWAP Orders
```python
from src.advanced.twap import TWAPOrder

twap_order = TWAPOrder(client)

# Execute TWAP order
orders = twap_order.execute_twap(
    symbol='BTCUSDT',
    total_quantity=0.01,
    num_chunks=5,
    interval_seconds=60,
    side='BUY'
)
```

## Logging

All actions are logged to `bot.log` with timestamps and detailed information about order executions and any errors that occur.

## Error Handling

The bot includes comprehensive input validation and error handling:
- Symbol validation
- Quantity and price validation
- API error handling
- Detailed error logging

## Disclaimer

This bot is for educational purposes only. Trading cryptocurrency futures carries significant risk. Always test thoroughly with small amounts first.