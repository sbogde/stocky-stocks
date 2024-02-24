// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({ value: '', image: '' });

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
        <img src={`${process.env.PUBLIC_URL}/data/images/${data.image}`} alt="Display"   className="responsive-image"/> 
      </header>
    </div>
  );
}

export default App;
