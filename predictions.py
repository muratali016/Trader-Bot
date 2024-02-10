import kucoin.client as kc
from kucoin.client import Trade
from kucoin.client import Market
import pandas as pd
from tech_analysis import TechnicalAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.pipeline import make_pipeline
import requests
import time
import matplotlib.pyplot as plt
import datetime
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy as np
from statsmodels.tsa.arima.model import ARIMA 
from pmdarima import auto_arima
from scipy import stats
import statsmodels


def send_to_telegram(message):
    apiToken = '5885423479:AAGUh7FnJe_ieChNfTnoOcPwQ__uCp_-5wo'
    chatID = '-1001906057801'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

api_key = '65b1770ea65b230001a65816'
api_secret = '3114f7d7-c8f5-49b0-b34f-f02dc27d8293'
api_passphrase = 'murat123'
 
#Symbol_list=["BTC-USDT"]
#time_intervals=["3min"]
from IPython.display import display
import calendar

#unix_timestamp = time.time()
#one_month_ago = datetime.fromtimestamp(unix_timestamp) - timedelta(days=90)
#one_month_ago_unix_timestamp = one_month_ago.timestamp()
#
#print(one_month_ago_unix_timestamp)
#print(unix_timestamp)

def create_csv(Symbol_list,time_intervals,unix_timestamp,one_month_ago_unix_timestamp):
    for symboll in Symbol_list:
        symbol=symboll
        m_client = Market(url='https://api.kucoin.com')
        for time_intervall in time_intervals:
            time_interval=time_intervall
            time.sleep(5)

            btc = m_client.get_kline(symbol,startAt=int(one_month_ago_unix_timestamp),endAt=int(unix_timestamp) ,kline_type=time_interval)

            df = pd.DataFrame(btc, columns=['timestamp', 'open','close', 'high', 'low', 'volume','amount'])
            df['close'] = pd.to_numeric(df['close'])
            df['volume'] = pd.to_numeric(df['volume'])

            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df['hour_of_day'] = df['timestamp'].dt.hour
            df['price_change'] = df['close'].diff()  

            df['price_change_pct'] = df['price_change'] / df['close'].shift()  
            df['volume_change'] = df['volume'].diff()
            df['volume_change_pct'] = df['volume_change'] / df['volume'].shift()  

            df.dropna(inplace=True)
            target = 'close'
            features = ['hour_of_day', 'price_change_pct', 'volume_change_pct']
            Xdata = df['close'].values[::-1]

            model = auto_arima(Xdata, trace=True, error_action='ignore', suppress_warnings=True)
            model_fit=model.fit(Xdata)

            print(model_fit.summary())
            forecast = model.predict(n_periods=1)
            print("ARIMA forecast:",forecast)

            #classification = classify_arima_model(model)
            #print(f'The ARIMA model is: {classification}')  
            df.to_csv("data.csv",index=False)
    
            #if classification=="Great" or classification=="Good"  :
            predicted_price = forecast
            print(f"The predicted closing price is: {predicted_price}")
            current_hour = df['hour_of_day'].iloc[0]  
            current_price = df['close'].iloc[0]
            previous_price = df['close'].iloc[1]  
            current_volume = df['volume'].iloc[0] 
            previous_volume = df['volume'].iloc[1]

            print(current_hour)
            print(current_price)
            print(previous_price)  
            print(current_volume)
            print(previous_volume)

            price_change_pct = (current_price - previous_price) / previous_price
            volume_change_pct = (current_volume - previous_volume) / previous_volume
            current_time = df['timestamp'].iloc[0]
            percentage_potential=((current_price-predicted_price)*100) / predicted_price
            percentage_potential=percentage_potential*-1
            percentage_potential=float(percentage_potential)
            message=f"Data is so accurate! \nCoin: {symbol} \nCurrent price:{current_price} \nPredicted price: {predicted_price} in the next {time_interval} \nPotential change: {percentage_potential:.2f}%"
            display(message)
            trading_dataCopy=pd.read_csv("data.csv")
            _technical_analysis = TechnicalAnalysis(trading_dataCopy)
            # if 'bool(self.df_last["morning_star"].values[0])' not in df:
            _technical_analysis.add_all()
            _technical_analysis.add_adx_buy_signals()
            _technical_analysis.add_bbands_buy_signals()
            df_signal = _technical_analysis.get_df()
            df_signal.to_csv("data2.csv",index=False)
            return df_signal




