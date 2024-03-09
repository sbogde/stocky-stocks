# Stock Visualization Web App

This web application presents an interactive visualization of stock price data, leveraging both Matplotlib and Bokeh for graphical representations. It offers users the ability to toggle between static Matplotlib images and interactive Bokeh charts, showcasing the latest stock prices along with historical data.

## Features

- **Symbol Display:** Showcases the stock symbol for current data visualization.
- **Chart Toggling:** Users can switch between static Matplotlib images and interactive Bokeh charts for stock price visualization.
- **Historical Data Navigation:** Allows navigation through historical stock data by date, with buttons to move to the next or previous day's data.
- **Downloadable Data:** Provides a downloadable CSV of the stock's historical price data.
- **Dynamic Loading State:** Implements a tri-state logic to enhance user experience by reducing flicker: loading state, Matplotlib chart, and Bokeh chart.

## Technology Stack

- **Frontend:** React.js
- **Data Visualization:** Matplotlib for static charts, Bokeh for interactive charts.
- **Backend:** Python scripts for data fetching and processing, utilizing ARIMA for forecasting stock prices.
- **Deployment:** Netlify

## Local Development

To run this project locally:

1. Clone the repository.
2. Install dependencies: `npm install`.
3. Start the development server: `npm start`.
4. For backend setup, ensure Python is installed and run `python backend/script.py` to fetch the latest data.
