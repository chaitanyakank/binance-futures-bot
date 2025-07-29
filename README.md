# Binance Futures Trading Bot (Testnet)

This is a GUI-based trading bot for Binance Futures Testnet built with Python and Tkinter.

## ✅ Features
- Place MARKET, LIMIT, STOP_MARKET, STOP_LOSS_MARKET, TAKE_PROFIT_MARKET orders
- Supports BUY/SELL with adjustable quantity and price
- View result messages in a graphical interface
- Logs activity to `logs/gui_trading.log`

## 💻 How to Run
1. Install Python 3.x
2. Install the required package:


3. Set up `config.py`:
```python
API_KEY = "your_testnet_api_key"
API_SECRET = "your_testnet_api_secret"
BASE_URL = "https://testnet.binancefuture.com"


python gui_test.py


