# /backend/libs/charts/charts_matplotlib.py
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def save_stock_chart(prices, dates, value, filename="stock_price.png"):
    plt.figure(figsize=(10, 6))
    
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
