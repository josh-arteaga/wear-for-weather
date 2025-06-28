import React from 'react';
import ReactDOM from 'react-dom/client';
import WeatherOutfit from './src/components/WeatherOutfit';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <WeatherOutfit />
    </React.StrictMode>
);

<div className="max-w-md mx-auto p-4">
  <h1 className="text-2xl font-bold mb-4">What Should I Wear?</h1>

  <input
    type="text"
    placeholder="Enter your city"
    className="w-full p-2 mb-4 border rounded"
    value={location}
    onChange={(e) => setLocation(e.target.value)}
  />

  <button
    onClick={handleFetch}
    className="w-full bg-blue-600 hover:bg-blue-700 text-white p-2 rounded"
  >
    Get Recommendation
  </button>

  <div className="mt-6">
    {weather && (
      <div className="mb-4">
        <h2 className="text-lg font-semibold">Weather: {weather.description}</h2>
        <p>Temperature: {weather.temp}°F</p>
      </div>
    )}

    {recommendation && (
      <div className="bg-gray-100 p-4 rounded shadow">
        <p>{recommendation}</p>
      </div>
    )}
  </div>
</div>
