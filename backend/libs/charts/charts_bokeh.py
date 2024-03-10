# /backend/libs/charts/charts_bokeh.py
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter
from datetime import timedelta
import pandas as pd

def save_bokeh_stock_chart(prices, dates, value, filename="bokeh_stock_chart.html"):
    """Save the stock prices chart as an interactive Bokeh plot, with dates on the x-axis."""
    # Convert string dates to datetime objects
    dates_dt = pd.to_datetime(dates)

    model_type = "LSTM" if "_lstm_" in filename else "ARIMA"
    
    # Prepare data
    source = ColumnDataSource(data=dict(date=dates_dt, price=prices))
    
    # Create a new plot with a title and axis labels
    p = figure(title="Random Stock Price (Bokeh)", x_axis_label='Date', y_axis_label='Price',
               x_axis_type='datetime', sizing_mode="stretch_width", height=450)
    
    # Add a line renderer with legend and line thickness
    p.line(x='date', y='price', source=source, legend_label="Stock Price", line_width=2)
    
   
    # Predicted value should be placed one day after the last date in the dataset
    predicted_date = dates_dt[-1] + timedelta(days=1)
    p.circle(predicted_date, value, size=7, color="red", legend_label=f"Predicted Value with {model_type}: {value}")


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
            '@date': 'datetime',
        },
        mode='vline'
    ))
    
    # Move the legend to the top left
    p.legend.location = "top_left"
    
    # Save the plot as an HTML file
    output_file(filename)
    save(p)
