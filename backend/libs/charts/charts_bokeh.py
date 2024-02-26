# /backend/libs/charts/charts_bokeh.py
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter
import pandas as pd


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
