import json
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os
import pandas as pd
import random
import subprocess
import yfinance as yf

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import DatetimeTickFormatter
from datetime import datetime, timedelta



def load_symbol_from_json():
    json_file_path = os.path.join('public', 'data', 'data.json')
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data.get('symbol', 'TEST')  # Default to 'TEST' if not found
    except FileNotFoundError:
        print("data.json file not found, defaulting to 'TEST'")
        return 'TEST'


def save_bokeh_stock_chart(prices, dates, value, filename="bokeh_stock_chart.html"):
    """Save the stock prices chart as an interactive Bokeh plot, with dates on the x-axis."""
    # Convert string dates to datetime objects
    dates_dt = pd.to_datetime(dates)
    
    # Prepare data
    source = ColumnDataSource(data=dict(date=dates_dt, price=prices))
    
    # Create a new plot with a title and axis labels
    p = figure(title="Random Stock Price (Bokeh)", x_axis_label='Date', y_axis_label='Price',
               x_axis_type='datetime', sizing_mode="stretch_width", height=450)
    
    # Add a line renderer with legend and line thickness
    p.line(x='date', y='price', source=source, legend_label="Stock Price", line_width=2)
    
    # Add a circle renderer for the random value point
    midpoint_index = len(prices) // 2
    midpoint_date = dates_dt[midpoint_index]
    p.circle(midpoint_date, value, size=7, color="red", legend_label=f"Value: {value}")

    # Customize the x-axis date formatting
    p.xaxis.formatter=DatetimeTickFormatter(
        days=["%d.%m.%y"],
        months=["%d.%m.%y"],
        years=["%d.%m.%y"],
    )

    # Add hover tool
    p.add_tools(HoverTool(
        tooltips=[
            ("Price", "@price"),
            ("Date", "@date{%F}")
        ],
        formatters={
            '@date': 'datetime',  # use 'datetime' formatter for '@date' field
        },
        mode='vline'
    ))
    
    # Save the plot as an HTML file
    output_file(filename)
    save(p)


def get_formatted_timestamp(format_str="%Y%m%d-%H%M%S"):
    """Returns a formatted timestamp string."""
    return datetime.now().strftime(format_str)


def run_git_command(command):
    """Runs a git command and returns its output"""
    try:
        output = subprocess.check_output(["git"] + command, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running git command {' '.join(command)}:\n{e.output.decode()}")


def git_commit_and_push():
    """Commit and push all changes to Git."""
    timestamp = get_formatted_timestamp("%Y-%m-%d %H:%M:%S")
    commit_message = f"Update data and image: {timestamp}"
    
    # Run Git command to add all changes
    run_git_command(["add", "."])
    
    # Commit and push
    run_git_command(["commit", "-m", commit_message])
    run_git_command(["push"])


def fetch_stock_prices(symbol):
    try:
        # Calculate dates for the last 35 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Format dates in YYYY-MM-DD format
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Fetch the stock data
        stock_data = yf.download(symbol, start=start_date_str, end=end_date_str)
        
        if stock_data.empty:
            print(f"No data found for symbol: {symbol}")
            return [], []
        
        # Reset the index to convert 'Date' from index to a column
        stock_data.reset_index(inplace=True)
        
        # Round the 'Close' prices to 2 decimals
        stock_data['Close'] = stock_data['Close'].round(2)
        
        # Prepare the CSV file path
        csv_directory = os.path.join('public', 'data', 'csvs')
        os.makedirs(csv_directory, exist_ok=True)  # Ensure the directory exists
        csv_filename = os.path.join(csv_directory, f"{symbol}.csv")
        
        # Save to CSV with only 'Date' and 'Close', no index
        stock_data[['Date', 'Close']].to_csv(csv_filename, index=False)
        
        # Extract dates as strings and 'Close' prices for plotting
        dates = stock_data['Date'].dt.strftime('%Y-%m-%d').tolist()
        prices = stock_data['Close'].tolist()

        return prices, dates


    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return []



def save_stock_chart(prices, dates, value, filename="stock_price.png"):
    plt.figure(figsize=(10, 6))
    
    # Since 'dates' are already strings, no need to format them again
    # dates = [date.strftime('%Y-%m-%d') for date in dates]  # This line is now unnecessary

    plt.plot(dates, prices, label='Stock Price', marker='.', linestyle='-', markersize=5)

    midpoint = len(prices) // 2
    value_date = dates[midpoint]  # Directly use 'dates' since they're already formatted
    plt.plot(value_date, value, 'ro', label=f'Value: {value}', markersize=8)

    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.gcf().autofmt_xdate()

    plt.title("Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig(filename)
    plt.close()


def update_json_value(image_filename, value, key):
    json_file_path = os.path.join('public', 'data', 'data.json')
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    data['value'] = str(value)
    data[key] = image_filename  # Use the key parameter to dynamically set the property
    
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)
        


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
    # save_bokeh_stock_chart(prices, random_value, os.path.join('public', 'data', 'images', bokeh_filename))
    save_bokeh_stock_chart(prices, dates, random_value, os.path.join('public', 'data', 'images', bokeh_filename))

    # Update data.json with Bokeh chart info (under a different key)
    update_json_value(bokeh_filename, random_value, 'bokeh_image')

    # Call the function to commit and push changes
    # git_commit_and_push()

