import json
import random
import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool

def save_bokeh_stock_chart(prices, value, filename="bokeh_stock_chart.html"):
    """Save the stock prices chart as an interactive Bokeh plot."""
    # Prepare data
    x_values = list(range(len(prices)))
    y_values = prices
    source = ColumnDataSource(data=dict(x=x_values, y=y_values))
    
    # Create a new plot with a title and axis labels
    p = figure(title="Random Stock Price (Bokeh)", x_axis_label='Time', y_axis_label='Price', sizing_mode="stretch_width", max_width=500, height=400)
    
    # Add a line renderer with legend and line thickness
    p.line('x', 'y', source=source, legend_label="Stock Price", line_width=2)
    
    # Add a circle renderer for the random value point
    midpoint = len(prices) // 2
    p.circle([midpoint], [value], size=10, color="red", legend_label=f"Value: {value}")
    
    # Add hover tool
    p.add_tools(HoverTool(tooltips=[("Time", "@x"), ("Price", "@y")], mode='vline'))
    
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


def generate_random_stock_prices(length=100):
    """Generate a list of random stock prices for plotting."""
    prices = [random.uniform(100, 500) for _ in range(length)]
    for i in range(1, length):
        # Randomly adjust the direction of the stock price slightly
        change = random.uniform(-5, 5)
        prices[i] = prices[i-1] + change
    return prices


def save_stock_chart(prices, value, filename="stock_price.png"):
    """Save the stock prices chart to a file, marking the 'value' with a red circle."""
    plt.figure(figsize=(10, 6))
    plt.plot(prices, label='Stock Price')  # Plot the stock prices
    
    # Determine the midpoint for the x-axis
    midpoint = len(prices) // 2  
    
    # Mark the random value with a red circle and include the value in the legend
    plt.plot(midpoint, value, 'ro', label=f'Value: {value}')  # Using an f-string for dynamic label
    
    plt.title("Stock Price")
    plt.xlabel("Time")
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
    matplotlib_filename = f"random_stock_chart_{timestamp_str}.png"
    bokeh_filename = f"bokeh_stock_chart_{timestamp_str}.html"
    
    # Generate random stock prices
    prices = generate_random_stock_prices()
    random_value = round(random.uniform(min(prices) * 0.9, max(prices) * 1.1), 2)
    
    # Generate and save the matplotlib chart
    save_stock_chart(prices, random_value, os.path.join('public', 'data', 'images', matplotlib_filename))
    
    # Update data.json with matplotlib chart info
    update_json_value(matplotlib_filename, random_value, 'matplotlib_image')
    
    # Generate and save the Bokeh chart
    save_bokeh_stock_chart(prices, random_value, os.path.join('public', 'data', 'images', bokeh_filename))
    
    # Update data.json with Bokeh chart info (under a different key)
    update_json_value(bokeh_filename, random_value, 'bokeh_image')

    # Call the function to commit and push changes
    # git_commit_and_push()

