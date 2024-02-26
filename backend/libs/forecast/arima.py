# /backend/libs/forecast/arima.py
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_with_arima(prices, order=(1, 1, 1)):
    """
    Forecast the next value in a series using the ARIMA model.

    Parameters:
    - prices: List of historical prices.
    - order: Tuple of the order (p, d, q) of the model.

    Returns:
    - The forecasted next value.
    """
    # Convert the prices to a pandas Series
    series = pd.Series(prices)
    
    # Fit the ARIMA model
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    
    # Forecast the next value
    forecast = model_fit.forecast(steps=1)

    # Round the forecast to 2 decimal places before returning
    forecasted_value = round(forecast.iloc[0], 2)
    
    return forecasted_value
