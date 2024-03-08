# /backend/script.py
import warnings

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from libs.charts.chart_factory import generate_charts

from libs.data.data_ops import load_symbol_from_json, fetch_stock_prices, update_json_value
from libs.git.git_ops import git_commit_and_push
from libs.misc.misc import get_formatted_timestamp
from libs.forecast.arima import forecast_with_arima
from libs.forecast.lstm import forecast_with_lstm
import os
import random


def main():
    # Generate unique filenames for both models' charts
    timestamp_str = get_formatted_timestamp()
    matplotlib_filename_arima = f"matplot_arima_chart_{timestamp_str}.png"
    bokeh_filename_arima = f"bokeh_arima_chart_{timestamp_str}.html"
    matplotlib_filename_lstm = f"matplot_lstm_chart_{timestamp_str}.png"
    bokeh_filename_lstm = f"bokeh_lstm_chart_{timestamp_str}.html"
    
    # Fetch stock prices
    symbol = load_symbol_from_json()
    prices, dates = fetch_stock_prices(symbol)
    last_date = dates[-1]  # The last date from the fetched stock prices

    # Forecast with ARIMA and LSTM
    forecasted_value_arima = forecast_with_arima(prices)
    forecasted_value_lstm = forecast_with_lstm(prices)
    print(f"Forecasted value with ARIMA: {forecasted_value_arima}")
    print(f"Forecasted value with LSTM: {forecasted_value_lstm}")
    
    # Generate charts for ARIMA
    generate_charts(prices, dates, forecasted_value_arima, os.path.join('public', 'data', 'images', matplotlib_filename_arima), os.path.join('public', 'data', 'images', bokeh_filename_arima))
    
    # Generate charts for LSTM
    generate_charts(prices, dates, forecasted_value_lstm, os.path.join('public', 'data', 'images', matplotlib_filename_lstm), os.path.join('public', 'data', 'images', bokeh_filename_lstm))
    
    # Update data.json with matplotlib & Bokeh charts
    # update_json_value(last_date, matplotlib_filename, bokeh_filename, forecasted_value_arima)
    update_json_value(
        last_date,
        matplotlib_filename_arima,
        bokeh_filename_arima,
        matplotlib_filename_lstm,
        bokeh_filename_lstm,
        forecasted_value_arima,
        forecasted_value_lstm
    )

    # Call the function to commit and push changes
    # git_commit_and_push()


if __name__ == "__main__":
    main()