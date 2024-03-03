import React, { useState, useEffect } from "react";
import "./App.css";
import logo from "./logo.png";

function App() {
  const [historicalData, setHistoricalData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentData, setCurrentData] = useState({
    symbol: "",
    value: "",
    matplotlib_image: "",
    bokeh_image: "",
  });
  const [showBokeh, setShowBokeh] = useState(true);
  const [isBokehLoading, setIsBokehLoading] = useState(true);

  function toggleChart() {
    setShowBokeh(!showBokeh);

    // Reset loading state every time we toggle the chart type - for testing purposes only
    // setIsBokehLoading(true);
    // setTimeout(() => {
    //   setIsBokehLoading(false);
    // }, 2000);
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

        // Simulate toggling after a delay
        setTimeout(() => {
          setShowBokeh(false);
          setTimeout(() => {
            setShowBokeh(true);
          }, 200);
        }, 200);
      });
  }, []);

  useEffect(() => {
    if (
      historicalData.length > 0 &&
      currentIndex >= 0 &&
      currentIndex < historicalData.length
    ) {
      setCurrentData({
        symbol: currentData.symbol, // keep the symbol unchanged
        ...historicalData[currentIndex],
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentIndex, historicalData]);

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

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div className="logo">Stocky Stocks ({currentData.symbol})</div>
        <p>
          {currentData.value} - {currentData.date}
        </p>

        <div className="buttons-container">
          {currentIndex < historicalData.length - 1 ? (
            <button onClick={goToPreviousDay}>Previous Day</button>
          ) : (
            // Disabled button instead of invisible
            <button disabled>Previous Day</button>
          )}
          <button onClick={toggleChart} className="button-show">
            Show {showBokeh ? "Matplotlib Image" : "Bokeh Chart"}
          </button>
          {currentIndex > 0 ? (
            <button onClick={goToNextDay}>Next Day</button>
          ) : (
            // Disabled button instead of invisible
            <button disabled>Next Day</button>
          )}
        </div>

        {showBokeh ? (
          <>
            {isBokehLoading && <div>Loading chart...</div>}
            <object
              data={`${process.env.PUBLIC_URL}/data/images/${currentData.bokeh_image}`}
              type="text/html"
              style={{
                width: "100%",
                height: "500px",
                display: "block",
                margin: "0 auto",
              }}
              aria-label="Interactive Bokeh chart displaying stock price data"
              onLoad={() => setIsBokehLoading(false)}
            >
              <p>Interactive Bokeh chart not supported by your browser.</p>
            </object>
          </>
        ) : (
          <img
            src={`${process.env.PUBLIC_URL}/data/images/${currentData.matplotlib_image}`}
            alt="Matplotlib Display"
            className="responsive-image"
          />
        )}
      </header>
    </div>
  );
}

export default App;
