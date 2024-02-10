import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Load your dataset (replace 'your_data.csv' with your actual file name)
#data = pd.read_csv('data2.csv', parse_dates=['timestamp'], index_col='timestamp')

def signal_class(data):
    def moving_average_crossover_strategy(data, short_window=5, long_window=20):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1, center=False).mean()

        signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1, center=False).mean()

        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], -1.0, 0.0)

        signals['positions'] = signals['signal'].diff()

        return signals
    
    signals = moving_average_crossover_strategy(data)

    data['signal'] = signals['positions'].shift(-1)  # Shift to align with the next period

    data = data.dropna()

    features = ['sma5', 'sma8', 'sma13', 'sma20', 'sma50', 'sma200']
    X = data[features]
    y = data['signal']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Evaluate the model performance
    #print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    #print('\nClassification Report:')
    #print(classification_report(y_test, y_pred))
    decision_scores=classification_report(y_test, y_pred)


    y_proba = model.predict_proba(X_test)
    #print(y_proba)
    # Map class labels to class names
    class_labels = model.classes_
    class_names = {1: "No Action", 0: "Sell", 2: "Buy"}


    predicted_class = np.argmax(y_proba, axis=1)
    #print(predicted_class)
    predicted_class_names = [class_names[label] for label in predicted_class]


    from collections import Counter
    element_counts = Counter(predicted_class_names)
    most_common_element = element_counts.most_common(1)[0][0]
    #print(most_common_element)
    print(decision_scores)

    last_data = data.head(1)  # Assuming this is the last available data point
    print(last_data)
    last_features = last_data[features]  # Select relevant features for prediction
    next_signal = model.predict(last_features)[0] 
    return next_signal


