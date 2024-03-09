# /backend/script.py
import warnings

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from libs.charts.charts_bokeh import save_bokeh_stock_chart
from libs.charts.charts_matplotlib import save_stock_chart
from libs.data.data_ops import load_symbol_from_json, fetch_stock_prices, update_json_value
from libs.git.git_ops import git_commit_and_push
from libs.misc.misc import get_formatted_timestamp
from libs.forecast.arima import forecast_with_arima
import os
import random


def main():
    # Generate unique filenames for both charts
    timestamp_str = get_formatted_timestamp()
    matplotlib_filename = f"matplot_stock_chart_{timestamp_str}.png"
    bokeh_filename = f"bokeh_stock_chart_{timestamp_str}.html"
    
    # Fetch stock prices
    symbol = load_symbol_from_json()
    prices, dates = fetch_stock_prices(symbol)
    last_date = dates[-1]  # The last date from the fetched stock prices

    # Use ARIMA to forecast the next value instead of using a random value
    forecasted_value = forecast_with_arima(prices)
    print(f"Forecasted value: {forecasted_value}")
    
    # Generate and save the matplotlib chart
    save_stock_chart(prices, dates, forecasted_value, os.path.join('public', 'data', 'images', matplotlib_filename))
    
    # Generate and save the Bokeh chart
    save_bokeh_stock_chart(prices, dates, forecasted_value, os.path.join('public', 'data', 'images', bokeh_filename))

    # Update data.json with matplotlib & Bokeh charts
    update_json_value(last_date, matplotlib_filename, bokeh_filename, forecasted_value)


    # Call the function to commit and push changes
    # git_commit_and_push()


if __name__ == "__main__":
    main()