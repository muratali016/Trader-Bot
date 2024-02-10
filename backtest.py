import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your dataset (replace 'data2.csv' with your actual file name)
data = pd.read_csv('data2.csv', parse_dates=['timestamp'], index_col='timestamp')


def moving_average_crossover_strategy(data, short_window=5, long_window=20):
    
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1, center=False).mean()
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], -1.0, 0.0)
    signals['positions'] = signals['signal'].diff()

    return signals


signals = moving_average_crossover_strategy(data)


starting_capital = 10000  
capital = starting_capital  
position = 0 

capital_over_time = [] 

for i in range(len(signals)):
    if signals['positions'][i] == -1.0:  # Sell signal
        position = capital / data['close'][i]
        capital = 0
    elif signals['positions'][i] == 1.0:  # Buy signal
        capital = position * data['close'][i]
        position = 0
    capital_over_time.append(capital)
 
plt.figure(figsize=(10, 6))
plt.plot(data['close'], label='Close Price')
plt.plot(signals.loc[signals['positions'] == -1.0].index, data['close'][signals['positions'] == -1.0], 'v', markersize=10, color='r', label='Sell Signal')
plt.plot(signals.loc[signals['positions'] == 1.0].index, data['close'][signals['positions'] == 1.0], '^', markersize=10, color='g', label='Buy Signal')
plt.title('Moving Average Crossover Strategy with Backtesting')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()


final_capital = capital if position == 0 else position * data['close'][-1]
print(f'Final Capital: ${final_capital:.2f}')

#plt.figure(figsize=(10, 6))
#plt.plot(capital_over_time)
#plt.title('Capital Changes Over Time')
#plt.xlabel('Trade Number')
#plt.ylabel('Capital ($)')
#plt.show()

 























#
#from predictions import create_csv
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from sklearn.linear_model import LogisticRegression
#
## Assuming you already have 'data' and 'signals' from your previous code
#
## Feature Engineering: Add moving averages as features
#data['short_mavg'] = data['close'].rolling(window=5, min_periods=1, center=False).mean()
#data['long_mavg'] = data['close'].rolling(window=20, min_periods=1, center=False).mean()
#
## Create binary labels for the classifier (1 for Buy, 0 for Hold or Sell)
#signals['label'] = np.where(signals['positions'] == -1.0, 0, np.where(signals['positions'] == 1.0, 1, 0))
#
## Combine features and labels
#features = data[['short_mavg', 'long_mavg']]
#labels = signals['label']
#
## Create and train a logistic regression model
#model = LogisticRegression(random_state=42)
#model.fit(features, labels)
#
## Use the trained model to predict the next step for the latest available data
#latest_data = data.head(1)  # Assuming this is the latest available data point
#latest_features = latest_data[['short_mavg', 'long_mavg']]
#next_step_probability = model.predict_proba(latest_features)[:, 1]  # Probability of the next step being a 'buy'
#
## Make a trading decision based on the predicted probability
#threshold = 0.5  # Adjust the threshold based on your risk tolerance
#predicted_action = "Buy" if next_step_probability > threshold else "Sell or Hold"
#
## Visualize the predicted probability and action
#plt.figure(figsize=(10, 6))
#plt.plot(data['close'], label='Close Price')
#scatter = plt.scatter(latest_data.index, latest_data['close'], c=next_step_probability, cmap='viridis', marker='o', label='Predicted Probability')
#plt.axhline(y=latest_data['close'].values[0], color='r', linestyle='--', label='Predicted Value')
#
## Annotate the predicted value on the scatter plot
#predicted_value = latest_data['close'].values[0]
#plt.annotate(f'Predicted Value: {predicted_value:.2f}', 
#             xy=(latest_data.index[0], predicted_value), 
#             xytext=(latest_data.index[0], predicted_value + 5),
#             arrowprops=dict(facecolor='black', shrink=0.05),
#             )
#
#plt.colorbar(scatter, label='Probability of Next Step (Buy)')
#plt.title(f'Next Step Prediction: {predicted_action}')
#plt.xlabel('Date')
#plt.ylabel('Close Price')
#plt.legend()
#plt.show()
#