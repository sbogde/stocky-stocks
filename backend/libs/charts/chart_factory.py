from .charts_matplotlib import save_stock_chart as save_matplotlib_chart
from .charts_bokeh import save_bokeh_stock_chart as save_bokeh_chart

def generate_charts(prices, dates, forecasted_value, matplotlib_filename, bokeh_filename):
    """
    Wrapper function to generate both Matplotlib and Bokeh charts.

    :param prices: List of stock prices.
    :param dates: Corresponding dates for the stock prices.
    :param forecasted_value: The forecasted stock price value.
    :param matplotlib_filename: Filename for the Matplotlib chart.
    :param bokeh_filename: Filename for the Bokeh chart.
    """

    forecasted_value = round(forecasted_value, 2)

    # Generate and save the matplotlib chart
    save_matplotlib_chart(prices, dates, forecasted_value, matplotlib_filename)
    
    # Generate and save the Bokeh chart
    save_bokeh_chart(prices, dates, forecasted_value, bokeh_filename)
