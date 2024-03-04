import React, { useState, useEffect } from "react";
import "./App.css";
import logo from "./logo.png";

function App() {
  const [historicalData, setHistoricalData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentData, setCurrentData] = useState({
    symbol: "",
    date: "",
    value_arima: "",
    value_lstm: "",
    matplotlib_image_arima: "",
    bokeh_image_arima: "",
    matplotlib_image_lstm: "",
    bokeh_image_lstm: "",
  });
  const [forecastModel, setForecastModel] = useState("arima"); // "arima" or "lstm"
  const [showBokeh, setShowBokeh] = useState(true);

  function toggleForecastModel() {
    setForecastModel(forecastModel === "arima" ? "lstm" : "arima");
  }

  function toggleChart() {
    setShowBokeh(!showBokeh);
  }

  useEffect(() => {
    fetch("/data/data.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => response.json())
      .then((jsonData) => {
        setHistoricalData(jsonData.historical_data);
        setCurrentData({
          symbol: jsonData.symbol,
          ...jsonData.historical_data[0],
        });
      });
  }, []);

  useEffect(() => {
    if (
      historicalData.length > 0 &&
      currentIndex >= 0 &&
      currentIndex < historicalData.length
    ) {
      setCurrentData({
        symbol: currentData.symbol,
        ...historicalData[currentIndex],
      });
    }
  }, [currentIndex, historicalData, currentData.symbol]);

  const goToNextDay = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const goToPreviousDay = () => {
    if (currentIndex < historicalData.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const getImageKey = (baseKey) => `${baseKey}_${forecastModel}`;
  const getValueKey = () => `value_${forecastModel}`;

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div className="logo">Stocky Stocks ({currentData.symbol})</div>
        <p>
          Price predicted with {forecastModel.toUpperCase()}: $
          {currentData[getValueKey()]} on {currentData.date}
        </p>
        <div className="buttons-container">
          {currentIndex < historicalData.length - 1 && (
            <button onClick={goToPreviousDay}>Previous Day</button>
          )}

          <button onClick={toggleForecastModel}>
            Show {forecastModel === "arima" ? "LSTM" : "ARIMA"} Forecast
          </button>
          <button onClick={toggleChart}>
            Show {showBokeh ? "Matplotlib Chart" : "Bokeh Chart"}
          </button>

          {currentIndex > 0 && <button onClick={goToNextDay}>Next Day</button>}
        </div>
        {showBokeh ? (
          <object
            data={`${process.env.PUBLIC_URL}/data/images/${
              currentData[getImageKey("bokeh_image")]
            }`}
            type="text/html"
            style={{
              width: "100%",
              height: "500px",
              display: "block",
              margin: "0 auto",
            }}
            aria-label={`Interactive ${forecastModel.toUpperCase()} Bokeh chart displaying stock price data`}
          >
            <p>Interactive Bokeh chart not supported by your browser.</p>
          </object>
        ) : (
          <img
            src={`${process.env.PUBLIC_URL}/data/images/${
              currentData[getImageKey("matplotlib_image")]
            }`}
            alt={`${forecastModel.toUpperCase()} Matplotlib Display`}
            className="responsive-image"
          />
        )}
      </header>
    </div>
  );
}

export default App;
