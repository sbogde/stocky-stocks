import json
import random
import os
import matplotlib.pyplot as plt

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



def update_json_value(image_filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(base_dir, 'public', 'data', 'data.json')
    image_file_path = os.path.join(base_dir, 'public', 'data', 'images', image_filename)

    prices = generate_random_stock_prices()
    
    # Calculate min and max of the prices with a 10% margin
    min_price = min(prices) * 0.9
    max_price = max(prices) * 1.1

    # Ensure the random value falls within this adjusted range
    random_value = round(random.uniform(min_price, max_price), 2)
    
    # Proceed with updating data.json and saving the chart as before
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    data['value'] = str(random_value)
    data['image'] = image_filename

    save_stock_chart(prices, random_value, image_file_path)
    
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)



if __name__ == "__main__":
    image_filename = "random_stock_chart.png" # You can include a timestamp to make filenames unique
    update_json_value(image_filename)
