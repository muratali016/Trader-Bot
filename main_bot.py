from signals_model import signal_class
from predictions import create_csv
import time
from datetime import datetime, timedelta
from kucoin.client import Trade
from kucoin.client import Market
from time import sleep
import sys
import logging
import gspread
from tkinter import messagebox
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

api_key = 'x'
api_secret = 'x'
api_passphrase = 'x'
 
m_client = Market(url='https://api.kucoin.com')
client = Trade(api_key, api_secret, api_passphrase)
coin = "BTC-USDT"
btc = m_client.get_all_tickers()
for info in btc["ticker"]:
    if info['symbol'] == coin:
        btc_usdt_sell = info['sell']
        btc_usdt_buy = info['buy']
btc_usdt_sell = float(btc_usdt_sell)
btc_usdt_buy = float(btc_usdt_buy)
purchase_price = btc_usdt_sell

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'tradingbot-388122-bf66d2bf966b.json', scope)
client_gs = gspread.authorize(creds)
worksheet = client_gs.open('TRADINGRESULTS').sheet1


Symbol_list=["BTC-USDT"]
time_intervals=["5min"]
coin = "BTC-USDT"
trading_value = 100
profit_percentage = 2
time_interval = 4
prevent_loss_percentage = -2
signal_list=[]
inventory=[]
profits=[]

while True:
    
    unix_timestamp = time.time()
    one_month_ago = datetime.fromtimestamp(unix_timestamp) - timedelta(days=900)
    one_month_ago_unix_timestamp = one_month_ago.timestamp()

    print(one_month_ago_unix_timestamp)
    print(unix_timestamp)

    data=create_csv(Symbol_list,time_intervals,unix_timestamp,one_month_ago_unix_timestamp)
     
    classs=signal_class(data)
    signal_list.append(classs)
    
    next_signal=signal_list[-1]
    print(next_signal)

    for info in btc["ticker"]:
        if info['symbol'] == coin:
            btc_usdt_sell = info['sell']
            btc_usdt_buy = info['buy']
            btc_usdt_sell = float(btc_usdt_sell)
            btc_usdt_buy = float(btc_usdt_buy)
    percent = (((purchase_price - btc_usdt_buy) *
                        100) / btc_usdt_buy)
    funds = trading_value
    print(next_signal)
    if next_signal==0.0:
        print( "No action")
        logging.info("No action")
        
    elif next_signal==1.0:
        try:
            btc = m_client.get_all_tickers()
            for info in btc["ticker"]:
                if info['symbol'] == coin:
                    btc_usdt_sell = info['sell']
                    btc_usdt_buy = info['buy']
                    btc_usdt_sell = float(btc_usdt_sell)
                    btc_usdt_buy = float(btc_usdt_buy)
                funds = trading_value
                sleep(2)
                #order = client.create_market_order(
                #    coin, 'buy', funds=funds)
                order="order"
                #log_str = f"Coin bought with price:{funds}\n"
                #logging.info(log_str)
                sleep(time_interval)
                btc = m_client.get_all_tickers()
                for info in btc["ticker"]:
                    if info['symbol'] == coin:
                        btc_usdt_sell = info['sell']
                        btc_usdt_buy = info['buy']
                        btc_usdt_sell = float(btc_usdt_sell)
                        btc_usdt_buy = float(btc_usdt_buy)
                percent = (((purchase_price - btc_usdt_buy) *
                            100) / btc_usdt_buy)
                percent = percent * (-1)

                if not inventory: 
                    inventory.append({"coin": coin, "quantity": funds, "purchase_price": btc_usdt_buy})
                    log_str = f"Coin bought with price: {funds}\n"
                    logging.info(log_str)
                    sleep(time_interval)
                else:
                    print("Inventory not empty, skipping buy signal.")

                log_str = f'The price of selling Coin now:{btc_usdt_buy}\n'
                logging.info(log_str)
                log_str = f"Base price: {purchase_price}\n"
                #purchase_price = btc_usdt_sell
                logging.info(log_str)
                log_str = f"Percentage Move: {percent}\n"
                logging.info(log_str)
                
                date_upd = datetime.now()
                date_str_upd = str(date_upd)
                worksheet.append_row([date_str_upd, btc_usdt_buy, purchase_price, percent])
                break
        except Exception as e:
            print("buy signal error:",e)
            logging.info(e)

    elif next_signal==-1.0:
        if inventory:
            logging.info(
               f"Sell signal. The percentage move is at {percent}")
            funds_new = trading_value + \
                (funds * (percent / 100))
            percent_add = round(funds_new, 6)
            funds_new_str = str(percent_add)
            sleep(2)
            #order = client.create_market_order(
            #    coin, 'sell', funds=funds_new_str)
            order="order"
            log_str = f"Coin sold with new price:{funds_new_str}\n"
            logging.info(log_str)
            #check = client.get_order_details(
            #    orderId=order['orderId'])
            #log_str = f"Check: {check}\n"
            logging.info(log_str)
            btc = m_client.get_all_tickers()
            for info in btc["ticker"]:
                if info['symbol'] == coin:
                    btc_usdt_sell = info['sell']
                    btc_usdt_buy = info['buy']
                    btc_usdt_sell = float(
                        btc_usdt_sell)
                    btc_usdt_buy = float(btc_usdt_buy)
            purchase_price = btc_usdt_sell
            log_str = f"New base price: {purchase_price}\n"
            logging.info(log_str)
            date_upd =datetime.now()
            date_str_upd = str(date_upd)
            worksheet.append_row([date_str_upd, btc_usdt_buy, purchase_price, percent])
            profits.append(percent)
            inventory=[]
        else:
            print("Inventory is empty, skipping sell signal.")

        if percent < prevent_loss_percentage:
            logging.info(
               f"The trade requirement was not satisfied. The percentage move is at {percent}")
            sleep(1)
            #order = client.create_market_order(
            #    coin, 'sell', funds=funds)
            order="order"
            log_str = "Sold to prevent more losses\n"
            logging.info(log_str)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            trade_details = [timestamp, 'Not Satisfied', coin, purchase_price, btc_usdt_buy, percent, trading_value]
            worksheet.append_row(trade_details)
            worksheet.clear()
            messagebox.showwarning("Warning", "Selling to prevent more losses")
            sys.exit()
             
    
    print(inventory)
    logging.info(inventory)
    logging.info(profits)
    print(signal_list)
    time.sleep(180)









