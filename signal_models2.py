import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from collections import Counter

def moving_average_crossover_strategy(data, short_window=4, long_window=25):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0


    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1, center=False).mean()

    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], -1.0, 0.0)

    signals['positions'] = signals['signal'].diff()

    return signals

data=pd.read_csv("data2.csv",parse_dates=['timestamp'], index_col='timestamp')
signals=moving_average_crossover_strategy(data)

data['sma50'] = data['close'].rolling(window=50, min_periods=1).mean()
data['sma100'] = data['close'].rolling(window=100, min_periods=1).mean()
data['rsi'] = 100 - (100 / (1 + (data['close'].diff(1).clip(lower=0) / data['close'].diff(1).clip(upper=0)).rolling(window=14, min_periods=1).mean()))
data['macd'] = data['close'].ewm(span=12, adjust=False).mean() - data['close'].ewm(span=26, adjust=False).mean()
data['macd_signal'] = data['macd'].ewm(span=9, adjust=False).mean()


signals = moving_average_crossover_strategy(data)
data['signal'] = signals['positions'].shift(-1)  # Shift to align with the next period


data = data.dropna()


features = ['sma5', 'sma8', 'sma13', 'sma20', 'sma50', 'sma200', 'rsi', 'macd', 'macd_signal']
X = data[features]
y = data['signal']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print('\nClassification Report:')
print(classification_report(y_test, y_pred))

# Find the class with the highest probability for each prediction
y_proba = model.predict_proba(X_test)
class_names = {0: "No Action", 1: "Sell", 2: "Buy"}
predicted_class = np.argmax(y_proba, axis=1)
predicted_class_names = [class_names[label] for label in predicted_class]

# Calculate the most common predicted class
element_counts = Counter(predicted_class_names)
most_common_element = element_counts.most_common(1)[0][0]
#print(f'Most Common Predicted Class: {most_common_element}')


last_data = data.head(1)  # Assuming this is the last available data point
print(last_data)
last_features = last_data[features]  # Select relevant features for prediction
next_signal = model.predict(last_features)[0]  # Predict the next signal
 
import matplotlib.pyplot as plt
# Visualize the predicted signal
#plt.figure(figsize=(10, 6))
#plt.plot(data['close'], label='Close Price')
#plt.scatter(last_data.index, last_data['close'], c='r', marker='o', label='Last Available Close')
print("next_signal",next_signal)

# Annotate the predicted signal on the plot
#plt.annotate(f'Next Signal: {class_names[next_signal]}', 
#             xy=(last_data.index[0], last_data['close'].values[0]), 
#             xytext=(last_data.index[0], last_data['close'].values[0] + 5),
#             arrowprops=dict(facecolor='black', shrink=0.05),
#             )
#
#plt.title('Predicting the Next Close Price')
#plt.xlabel('Date')
#plt.ylabel('Close Price')
#plt.legend()
#plt.show()

#
#plt.figure(figsize=(10, 6))
#plt.plot(data.index, data['close'], label='Close Prices', color='blue')
#
# Highlight the buy (1) and sell (-1) signals
buy_signals = data[data['signal'] == 1]
sell_signals = data[data['signal'] == -1]

 

#
#plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='g', label='Buy Signal')
#plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='r', label='Sell Signal')
#
#plt.title('Trading Signals')
#plt.xlabel('Date')
#plt.ylabel('Closing Price')
#plt.legend()
#plt.show()