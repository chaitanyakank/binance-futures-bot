from binance.client import Client
from config import API_KEY, API_SECRET, BASE_URL
import logging

# Setup logging
logging.basicConfig(filename='logs/trading.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class BasicBot:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)
        self.client.FUTURES_URL = BASE_URL + "/fapi"
        self.client.API_URL = BASE_URL + "/fapi"
        print("✅ Connected to Binance Futures Testnet")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            if order_type == "MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=quantity
                )
            elif order_type == "LIMIT":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=quantity,
                    price=price
                )
            elif order_type == "STOP_MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="STOP_MARKET",
                    stopPrice=stop_price if stop_price else price,
                    timeInForce="GTC",
                    quantity=quantity,
                    priceProtect=True
                )
            elif order_type == "TAKE_PROFIT_MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="TAKE_PROFIT_MARKET",
                    stopPrice=stop_price if stop_price else price,
                    timeInForce="GTC",
                    quantity=quantity,
                    priceProtect=True
                )
            elif order_type == "STOP_LOSS_MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="STOP_LOSS_MARKET",
                    stopPrice=stop_price if stop_price else price,
                    timeInForce="GTC",
                    quantity=quantity,
                    priceProtect=True
                )
            else:
                logging.warning(f"Unsupported order type: {order_type}")
                print("❌ Unsupported order type.")
                return None

            logging.info(f"{order_type} order placed: {order}")
            print("✅", order_type, "order placed successfully!")
            print("Order ID:", order["orderId"])
            print("Status:", order["status"])
            return order

        except Exception as e:
            logging.error(f"Error placing order: {e}")
            print("❌ Error placing order:", e)
            return None

    def get_order_status(self, symbol, order_id):
        try:
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logging.info(f"Fetched order status: {order}")
            print("📦 Order Status:")
            print("Status:", order["status"])
            print("Executed Qty:", order["executedQty"])
            print("Price:", order["price"])
            print("Update Time:", order["updateTime"])
            return order
        except Exception as e:
            logging.error(f"Error fetching order status: {e}")
            print("❌ Error fetching order status:", e)
            return None


def show_menu():
    print("\n=== Binance Futures Trading Bot ===")
    print("Select Order Type:")
    print("1. MARKET")
    print("2. LIMIT")
    print("3. STOP_MARKET")
    print("4. TAKE_PROFIT_MARKET")
    print("5. STOP_LOSS_MARKET")
    print("0. Exit")


def get_user_input():
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter side (BUY or SELL): ").upper()

    while True:
        show_menu()
        choice = input("Enter choice number: ").strip()
        order_type_map = {
            "1": "MARKET",
            "2": "LIMIT",
            "3": "STOP_MARKET",
            "4": "TAKE_PROFIT_MARKET",
            "5": "STOP_LOSS_MARKET",
            "0": "EXIT"
        }
        if choice in order_type_map:
            order_type = order_type_map[choice]
            if order_type == "EXIT":
                print("Exiting...")
                return None, None, None, None, None
            break
        else:
            print("Invalid choice. Try again.")

    quantity = float(input("Enter quantity: "))
    price = None
    stop_price = None

    if order_type in ["LIMIT"]:
        price = float(input("Enter limit price: "))
    elif order_type in ["STOP_MARKET", "TAKE_PROFIT_MARKET", "STOP_LOSS_MARKET"]:
        stop_price = float(input("Enter stop price: "))

    return symbol, side, order_type, quantity, price, stop_price


if __name__ == "__main__":
    bot = BasicBot()
    user_input = get_user_input()
    if user_input[0] is None:
        exit()

    symbol, side, order_type, quantity, price, stop_price = user_input
    order = bot.place_order(symbol, side, order_type, quantity, price, stop_price)

    if order:
        # Ask user if they want to check order status
        check = input("Do you want to check order status? (yes/no): ").lower()
        if check == "yes":
            order_id = order["orderId"]
            bot.get_order_status(symbol, order_id)
