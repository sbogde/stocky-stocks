// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({ value: '', matplotlib_image: '', bokeh_image: '' });
  const [showBokeh, setShowBokeh] = useState(true); 

  function toggleChart() {
    setShowBokeh(!showBokeh); 
  }
  
  useEffect(() => {
    fetch('/data/data.json', {
      headers : { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
       }
    })
      .then((response) => response.json())
      .then((jsonData) => setData(jsonData));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <div className="logo">Stocky Stocks</div>
        <p>{data.value}</p>
        <button onClick={toggleChart}>
          Show {showBokeh ? 'Matplotlib Image' : 'Bokeh Chart'}
        </button>
        {showBokeh ? (
          <object
            data={`${process.env.PUBLIC_URL}/data/images/${data.bokeh_image}`}
            type="text/html"
            style={{ width: "100%", height: "500px", display: "block", margin: "0 auto" }}
            aria-label="Interactive Bokeh chart displaying stock price data">
              <p>Interactive Bokeh chart not supported by your browser.</p>
          </object>
        ) : (
          <img
            src={`${process.env.PUBLIC_URL}/data/images/${data.matplotlib_image}`}
            alt="Matplotlib Display"
            className="responsive-image"
          />
        )}
      </header>
    </div>
  );
  
}

export default App;
