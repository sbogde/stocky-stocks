# /backend/libs/data/data_ops.py
from datetime import datetime, timedelta
import json
import os
import yfinance as yf


def load_symbol_from_json():
    json_file_path = os.path.join('public', 'data', 'data.json')
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data.get('symbol', 'TEST')  # Default to 'TEST' if not found
    except FileNotFoundError:
        print("data.json file not found, defaulting to 'TEST'")
        return 'TEST'
    


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




def update_json_value(last_date, matplotlib_filename_arima, bokeh_filename_arima,
                      matplotlib_filename_lstm, bokeh_filename_lstm, value_arima, value_lstm):
    json_file_path = os.path.join('public', 'data', 'data.json')

    # Load or initialize the JSON file structure
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {"symbol": "CB", "historical_data": []}

    # Check if the provided date already exists in historical_data
    existing_entry = next((entry for entry in data["historical_data"] if entry["date"] == last_date), None)

    if existing_entry:
        # Update the existing entry with the new data for both ARIMA and LSTM
        existing_entry["value_arima"] = str(value_arima)
        existing_entry["matplotlib_image_arima"] = matplotlib_filename_arima
        existing_entry["bokeh_image_arima"] = bokeh_filename_arima
        existing_entry["value_lstm"] = str(value_lstm)
        existing_entry["matplotlib_image_lstm"] = matplotlib_filename_lstm
        existing_entry["bokeh_image_lstm"] = bokeh_filename_lstm
    else:
        # Create a new entry for the provided date with both ARIMA and LSTM data
        new_entry = {
            "date": last_date,
            "value_arima": str(value_arima),
            "matplotlib_image_arima": matplotlib_filename_arima,
            "bokeh_image_arima": bokeh_filename_arima,
            "value_lstm": str(value_lstm),
            "matplotlib_image_lstm": matplotlib_filename_lstm,
            "bokeh_image_lstm": bokeh_filename_lstm
        }
        # Add the new entry to the start of the historical_data list
        data["historical_data"].insert(0, new_entry)

    # Write the updated data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

