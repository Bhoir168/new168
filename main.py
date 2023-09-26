from flask import Flask, render_template, request
from kite_trade import *
import logging
import time

app = Flask(__name__)

# Initialize the Kite API
kite = None  # We will initialize it later with user credentials


# Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Create an HTML template for the homepage


# Define the trading logic route
@app.route('/trade', methods=['POST'])
def trade():
    global kite  # Access the global variable

    # Retrieve user credentials and form data
    user_id = request.form['user_id']
    password = request.form['password']
    twofa = request.form['twofa']
    symbol = request.form['symbol']
    limit_price = float(request.form['limit_price'])

    # Initialize the Kite API with user credentials
    enctoken = get_enctoken(user_id, password, twofa)
    kite = KiteApp(enctoken=enctoken)

    # Get the current stock price
    stock_price = kite.ltp(f'NSE:{symbol}')[f'NSE:{symbol}']['last_price']

    if stock_price > limit_price:
        sell_order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                      exchange=kite.EXCHANGE_NSE,
                                      tradingsymbol=symbol,
                                      transaction_type=kite.TRANSACTION_TYPE_SELL,
                                      quantity=6,
                                      order_type=kite.ORDER_TYPE_MARKET,
                                      product=kite.PRODUCT_MIS)
        return f"SELL order placed with order id: {sell_order}"
    else:
        return "PENDING"


if __name__ == '__main__':
    app.run(debug=True)
