from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd  # Ensure pandas is imported

def save_stock_chart(prices, dates, value, filename="stock_price.png"):
    plt.figure(figsize=(10, 6))
    
    # Ensure 'dates' are datetime objects
    dates_dt = [pd.to_datetime(date) for date in dates]
    
    # Convert 'dates' to Matplotlib date format for plotting
    mpl_dates = mdates.date2num(dates_dt)  # Convert datetime objects to Matplotlib date format
    
    plt.plot(mpl_dates, prices, label='Stock Price', marker='.', linestyle='-', markersize=5)
    
    # Predicted value should be placed one day after the last date in the dataset
    predicted_date = dates_dt[-1] + timedelta(days=1)
    mpl_predicted_date = mdates.date2num(predicted_date)  # Convert to Matplotlib date format
    
    plt.plot(mpl_predicted_date, value, 'ro', label=f'Predicted Value: {value}', markersize=8)
    
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.gcf().autofmt_xdate()  # Rotate date labels to prevent overlap
    
    plt.title("Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc='upper left')
    plt.savefig(filename)
    plt.close()
