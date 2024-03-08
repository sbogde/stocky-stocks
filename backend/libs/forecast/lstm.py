
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def forecast_with_lstm(prices, look_back=1):
    """
    Forecast the next value in a series using an LSTM model.

    Parameters:
    - prices: List of historical prices.
    - look_back: Number of past time steps to use as input variables to predict the next time period.

    Returns:
    - The forecasted next value.
    """
    # Convert the prices to a numpy array and reshape
    data = np.array(prices).reshape(-1, 1)
    
    # Normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(data)
    
    # Prepare the dataset
    X, y = [], []
    for i in range(len(data)-look_back-1):
        a = data[i:(i+look_back), 0]
        X.append(a)
        y.append(data[i + look_back, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
    
    # Build and fit the LSTM model
    model = Sequential()
    model.add(LSTM(4, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=100, batch_size=1, verbose=2)
    
    # Forecast the next value
    last_features = np.array(prices[-look_back:]).reshape(1, 1, look_back)
    forecast = scaler.inverse_transform(model.predict(last_features))
    
    return round(forecast[0][0], 2)
