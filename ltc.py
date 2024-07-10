from binance.client import Client
from datetime import datetime, timedelta
import time
import configparser
from cryptography.fernet import Fernet
import getpass
import os

def load_key():
    key_file = "secret.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    return key

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def setup_api_keys():
    print("Please enter your Binance API key and secret key securely.")
    api_key = getpass.getpass("API Key: ")
    api_secret = getpass.getpass("API Secret: ")

    password = getpass.getpass("Enter password to secure your API keys: ")

    key = load_key()
    encrypted_api_key = encrypt_data(api_key, key)
    encrypted_api_secret = encrypt_data(api_secret, key)

    config = configparser.ConfigParser()
    config['binance'] = {
        'api_key': encrypted_api_key.decode(),
        'api_secret': encrypted_api_secret.decode()
    }

    with open('api.cfg', 'w') as configfile:
        config.write(configfile)

    print("API keys saved securely.")

def decrypt_api_keys():
    try:
        config = configparser.ConfigParser()
        config.read('api.cfg')

        encrypted_api_key = config.get('binance', 'api_key')
        encrypted_api_secret = config.get('binance', 'api_secret')

        password = getpass.getpass("Enter password to decrypt your API keys: ")
        key = load_key()

        api_key = decrypt_data(encrypted_api_key.encode(), key)
        api_secret = decrypt_data(encrypted_api_secret.encode(), key)

        return api_key, api_secret

    except Exception as e:
        print(f"Error decrypting API keys: {e}")
        return None, None

def initialize_binance_client():
    try:
        api_key, api_secret = decrypt_api_keys()
        if api_key and api_secret:
            client = Client(api_key, api_secret)
            return client
        else:
            print("Failed to initialize Binance client. Check API credentials.")
            return None
    except Exception as e:
        print(f"Error initializing Binance client: {e}")
        return None

symbol = 'LTCUSDT'
quantity = 1 
buy_threshold = 50
sell_threshold = 60
wait_period_hours = 24 
stop_loss_percent = 5 

def get_current_price(symbol, client):
    try:
        avg_price = client.get_avg_price(symbol=symbol)
        return float(avg_price['price'])
    except Exception as e:
        print(f"Error fetching current price: {e}")
        return None

def buy_litecoin(symbol, quantity, client):
    try:
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print(f"Buy order placed: {order}")
        return order
    except Exception as e:
        print(f"Error placing buy order: {e}")
        return None

def sell_litecoin(symbol, quantity, client):
    try:
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        print(f"Sell order placed: {order}")
        return order
    except Exception as e:
        print(f"Error placing sell order: {e}")
        return None

def wait_for_period(hours):
    print(f"Waiting for {hours} hours...")
    time.sleep(hours * 3600) 

def check_balance(symbol, client):
    try:
        account_info = client.get_account()
        for balance in account_info['balances']:
            if balance['asset'] == symbol:
                held_quantity = float(balance['free'])
                print(f"Currently holding {held_quantity} {symbol}.")
                return held_quantity
        print(f"Not holding any {symbol}.")
        return 0.0
    except Exception as e:
        print(f"Error checking {symbol} balance: {e}")
        return None

def run_trading_strategy(symbol, quantity, buy_threshold, sell_threshold, wait_period_hours, stop_loss_percent, client):
    try:
        held_quantity = check_balance(symbol, client)
        if held_quantity > 0:
            print(f"Already holding {held_quantity} {symbol}. Skipping buy.")
            return
        
        current_price = get_current_price(symbol, client)
        if current_price is None:
            return
        
        print(f"Current {symbol} price: ${current_price}")
        
        if current_price < buy_threshold:
            print(f"Current price (${current_price}) is below ${buy_threshold}. Buying {quantity} {symbol}...")
            buy_order = buy_litecoin(symbol, quantity, client)
            if buy_order is None:
                return
            
            wait_for_period(wait_period_hours)
            
            current_price_after_wait = get_current_price(symbol, client)
            if current_price_after_wait is None:
                return
            
            print(f"Price after {wait_period_hours} hours: ${current_price_after_wait}")
            
            if current_price_after_wait >= sell_threshold:
                print(f"Price has risen above ${sell_threshold}. Selling {quantity} {symbol} at ${current_price_after_wait}...")
                sell_order = sell_litecoin(symbol, quantity, client)
                if sell_order is None:
                    return
            elif current_price_after_wait <= (current_price * (1 - stop_loss_percent / 100)):
                print(f"Price has fallen below stop loss threshold ({stop_loss_percent}% loss). Selling {quantity} {symbol} at ${current_price_after_wait}...")
                sell_order = sell_litecoin(symbol, quantity, client)
                if sell_order is None:
                    return
        else:
            print(f"Current price (${current_price}) is not below ${buy_threshold}. Holding.")
    
    except Exception as e:
        print(f"Error in trading strategy: {e}")

if __name__ == "__main__":
    client = initialize_binance_client()
    if client:
        run_trading_strategy(symbol, quantity, buy_threshold, sell_threshold, wait_period_hours, stop_loss_percent, client)
    else:
        print("Failed to initialize Binance client. Exiting...")
