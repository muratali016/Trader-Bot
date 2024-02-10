# Trader-Bot
## Use and Invest at Your Own Risk

## Backtest
![Figure_1](https://github.com/muratali016/Trader-Bot/assets/77502485/ab15c5ba-8eaf-41f1-ae10-9f3158d266cb)


## Introduction

This Python script serves as the main component of a trading bot designed to automate cryptocurrency trading on the KuCoin exchange platform. The bot utilizes various signals and market data to make trading decisions, with the primary objective of generating profits.

## Dependencies

The script relies on the following Python libraries and modules:

- `signals_model`: Contains the `signal_class` used for analyzing market signals.
- `predictions`: Includes functions for generating predictions and creating CSV files.
- `time`: Provides functionality for time-related operations.
- `datetime`: Enables date and time manipulation.
- `kucoin.client`: Imports the Trade and Market classes for interacting with the KuCoin API.
- `sys`: Offers access to system-specific parameters and functions.
- `logging`: Facilitates logging for monitoring the bot's activities.
- `gspread`: Allows interaction with Google Sheets.
- `tkinter.messagebox`: Provides message box functionality for displaying warnings.

## Configuration

### API Credentials

The script requires API credentials to authenticate with the KuCoin exchange. Ensure that the following variables are correctly configured with your API key, API secret, and API passphrase:

- `api_key`
- `api_secret`
- `api_passphrase`

### Google Sheets Integration

To enable recording of trading results in a Google Sheets document, the script utilizes Google Sheets API. Make sure to set up a service account and provide the path to the service account JSON file in the following line:

```python
creds = ServiceAccountCredentials.from_json_keyfile_name('tradingbot-388122-bf66d2bf966b.json', scope)
```

Ensure that the specified Google Sheets document ('TRADINGRESULTS' in this case) exists and is accessible by the service account.

## Functionality

The script performs the following main functions:

- **Market Data Retrieval**: Fetches market data for the specified cryptocurrency pair (e.g., BTC-USDT) from the KuCoin exchange.
  
- **Signal Analysis**: Analyzes market signals using the `signal_class` from `signals_model` and generates trading signals.
  
- **Trading Execution**: Executes buy or sell orders based on the generated signals, considering parameters such as trading value, profit percentage, and prevent loss percentage.
  
- **Logging**: Logs trading activities, errors, and other relevant information to a log file ('trading_bot.log' in this case).
  
- **Google Sheets Recording**: Records trading results, including timestamps, prices, percentage moves, and trading values, in a Google Sheets document.
  
- **Continuous Execution**: The script runs indefinitely, periodically fetching market data, analyzing signals, and executing trades at specified intervals (e.g., every 3 minutes).

## Usage

Ensure that all necessary dependencies are installed and the configuration variables are properly set before running the script. Execute the script in a Python environment to start the trading bot.
