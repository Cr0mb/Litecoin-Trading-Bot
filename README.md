# Litecoin-Trading-Bot
This Python script automates trading on Binance using a simple strategy for the Litecoin (LTC) market. 

It fetches current prices, buys LTC when the price drops below a specified threshold, and sells LTC after a waiting period if the price rises above a sell threshold or falls below a stop-loss percentage.

## Disclaimer
This script is provided for educational purposes and as a template only. 

It interacts with real cryptocurrency exchanges (like Binance) and involves financial risks. 

Use it at your own risk. Ensure to thoroughly understand and test the script in a simulated environment before using it with real funds. 

The author has not tested this script with real funds or Litecoins.


## Features

- Secure API Key Management: Encrypts and securely stores Binance API keys locally.
- Automated Trading Strategy: Executes a predefined trading strategy for LTC based on configured thresholds and parameters.
- Error Handling and Logging: Provides robust error handling for API interactions and logs trading activities for review.
- Price Monitoring: Constantly monitors LTC prices and triggers buy/sell actions based on predefined conditions.
- Configurable Strategy Parameters: Easily adjustable parameters such as buy threshold, sell threshold, wait period, and stop-loss percentage.
- User Interaction: Prompts the user to securely input API keys and passwords during setup.
- Real-time Feedback: Prints detailed feedback on trading actions and errors encountered during execution.

## Requirements

Python 3.x
```
pip install python-binance cryptography
```

## Configuration
1. API Key Setup

> Run the script to securely enter your Binance API key and secret key.

> These keys are encrypted and saved in api.cfg using a password provided during setup.

2. Script Configuration

> Modify parameters like symbol, quantity, buy_threshold, sell_threshold, wait_period_hours, and stop_loss_percent to suit your trading strategy.


