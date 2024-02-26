# /backend/script.py
from libs.charts.charts_bokeh import save_bokeh_stock_chart
from libs.charts.charts_matplotlib import save_stock_chart
from libs.data.data_ops import load_symbol_from_json, fetch_stock_prices, update_json_value
from libs.git.git_ops import git_commit_and_push
from libs.misc.misc import get_formatted_timestamp
import os
import random



if __name__ == "__main__":
    # Generate unique filenames for both charts
    timestamp_str = get_formatted_timestamp()
    matplotlib_filename = f"matplot_stock_chart_{timestamp_str}.png"
    bokeh_filename = f"bokeh_stock_chart_{timestamp_str}.html"
    
    # Fetch stock prices
    symbol = load_symbol_from_json()
    prices, dates = fetch_stock_prices(symbol)
    random_value = round(random.uniform(min(prices) * 0.9, max(prices) * 1.1), 2)
    
    # Generate and save the matplotlib chart
    save_stock_chart(prices, dates, random_value, os.path.join('public', 'data', 'images', matplotlib_filename))
    
    # Update data.json with matplotlib chart info
    update_json_value(matplotlib_filename, random_value, 'matplotlib_image')
    
    # Generate and save the Bokeh chart
    save_bokeh_stock_chart(prices, dates, random_value, os.path.join('public', 'data', 'images', bokeh_filename))

    # Update data.json with Bokeh chart info (under a different key)
    update_json_value(bokeh_filename, random_value, 'bokeh_image')

    # Call the function to commit and push changes
    # git_commit_and_push()

