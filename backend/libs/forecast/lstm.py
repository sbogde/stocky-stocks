# /backend/libs/forecast/lstm.py

import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler

def forecast_with_lstm(prices, look_back=1):
    series = np.array(prices).reshape(-1, 1)

    # Normalize the data
    scaler = StandardScaler()
    scaler.fit(series[:len(series) // 2])
    series = scaler.transform(series).flatten()


    # Build the dataset
    T = 10
    D = 1
    X = []
    Y = []
    for t in range(len(series) - T):
        x = series[t:t+T]
        X.append(x)
        y = series[t+T]
        Y.append(y)

    X = np.array(X).reshape(-1, T, 1) # N x T x D data 💡
    Y = np.array(Y)
    N = len(X)

    i = Input(shape=(T, 1))
    x = LSTM(5)(i)
    x = Dense(1)(x)
    model = Model(i, x)
    model.compile(
        loss='mse',
        optimizer=Adam(lr=0.1),
    )

    # train the RNN 🚂
    r = model.fit(
        X[:-N//2], Y[:-N//2],
        epochs=80,
        validation_data=(X[-N//2:], Y[-N//2:]),
    )

    
    # Forecast the next value
    last_features = np.array(prices[-look_back:]).reshape(1, 1, look_back)
    forecast = scaler.inverse_transform(model.predict(last_features))
    
    return round(forecast[0][0], 2)
