import tkinter as tk
from binance.client import Client
from config import API_KEY, API_SECRET, BASE_URL
import logging

# Set up logging
logging.basicConfig(filename='logs/gui_trading.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Binance client
client = Client(API_KEY, API_SECRET)
client.FUTURES_URL = BASE_URL + "/fapi"
client.API_URL = BASE_URL + "/fapi"

# Create main window
window = tk.Tk()
window.title("Binance Futures Trading Bot")
window.geometry("400x450")

# === Input Fields ===
tk.Label(window, text="Symbol (e.g. BTCUSDT):").pack()
symbol_entry = tk.Entry(window)
symbol_entry.pack()

tk.Label(window, text="Side (BUY / SELL):").pack()
side_entry = tk.Entry(window)
side_entry.pack()

tk.Label(window, text="Order Type (MARKET / LIMIT / STOP_MARKET / TAKE_PROFIT_MARKET / STOP_LOSS_MARKET):").pack()
order_type_entry = tk.Entry(window)
order_type_entry.pack()

tk.Label(window, text="Quantity:").pack()
quantity_entry = tk.Entry(window)
quantity_entry.pack()

tk.Label(window, text="Price (if needed):").pack()
price_entry = tk.Entry(window)
price_entry.pack()

# === Output Label ===
result_label = tk.Label(window, text="", fg="blue")
result_label.pack(pady=10)

# === Order Function ===
def place_order():
    symbol = symbol_entry.get().upper()
    side = side_entry.get().upper()
    order_type = order_type_entry.get().upper()
    quantity = float(quantity_entry.get())
    price_input = price_entry.get()
    price = float(price_input) if price_input else None

    try:
        order_args = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type in ["LIMIT"]:
            order_args["price"] = price
            order_args["timeInForce"] = "GTC"
        elif order_type in ["STOP_MARKET", "STOP_LOSS_MARKET", "TAKE_PROFIT_MARKET"]:
            order_args["stopPrice"] = price
            order_args["timeInForce"] = "GTC"
            order_args["priceProtect"] = True

        order = client.futures_create_order(**order_args)
        result = f"✅ Order Placed: ID {order['orderId']} Status: {order['status']}"
        result_label.config(text=result)
        logging.info(f"Order placed: {order}")

    except Exception as e:
        error = f"❌ Error: {e}"
        result_label.config(text=error, fg="red")
        logging.error(error)

# === Button ===
submit_btn = tk.Button(window, text="Place Order", command=place_order)
submit_btn.pack(pady=20)

# Run GUI
window.mainloop()
