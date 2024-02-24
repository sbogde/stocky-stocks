// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({ value: '', matplotlib_image: '', bokeh_image: '' });


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
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <div className="logo">Stocky Stock</div>

        <p>{data.value}</p>
        {/* Update the image src to point to the public URL */}
        {/* <img src={`${process.env.PUBLIC_URL}/data/images/${data.matplotlib_image}`} alt="Display"   className="responsive-image"/>  */}
        {/* Embed the Bokeh chart using an object tag */}
        <object
  data={`${process.env.PUBLIC_URL}/data/images/${data.bokeh_image}`}
  type="text/html"
  style={{ width: "100%", height: "500px", display: "block", margin: "0 auto" }}
  aria-label="Interactive chart displaying stock price data">
    <p>Interactive chart displaying stock price data. Your browser does not support this chart.</p>
</object>
      </header>
    </div>
  );
}

export default App;
