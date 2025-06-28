import { useState } from 'react';

export default function WeatherOutfit() {
  const [location, setLocation] = useState('');
  const [weather, setWeather] = useState(null);
  const [recommendation, setRecommendation] = useState('');
  const [loading, setLoading] = useState(false);

  // TEMP: Hardcoded lat/lon for Austin, TX
  const hardcodedCoords = {
    lat: 30.2672,
    lon: -97.7431,
  };

  const handleGetRecommendation = async () => {
    setLoading(true);
    setWeather(null);
    setRecommendation('');

    try {
      const weatherRes = await fetch(
        `http://127.0.0.1:8000/weather?lat=${hardcodedCoords.lat}&lon=${hardcodedCoords.lon}`
      );

      if (!weatherRes.ok) throw new Error('Weather fetch failed');

      const weatherData = await weatherRes.json();
      setWeather(weatherData);

      console.log("Sending to /recommend:", weatherData);

      const llmRes = await fetch('http://127.0.0.1:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ weather: weatherData }),
      });

      if (!llmRes.ok) throw new Error('LLM fetch failed');

      const llmData = await llmRes.json();
      setRecommendation(llmData.outfit || 'No outfit suggestion found.');

    } catch (err) {
      console.error(err);
      setRecommendation('An error occurred fetching data.');
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-md mt-10">
      <h1 className="text-2xl font-bold mb-4 text-center">What Should I Wear?</h1>

      <input
        type="text"
        placeholder="Enter your city (future feature)"
        className="w-full p-2 mb-4 border border-gray-300 rounded"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        disabled
      />

      <button
        onClick={handleGetRecommendation}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        disabled={loading}
      >
        {loading ? 'Thinking...' : 'Get Recommendation'}
      </button>

      <div className="mt-6 space-y-4">
        {weather && (
          <div className="bg-gray-100 p-3 rounded">
            <h2 className="font-semibold text-lg">Weather</h2>
            <p>{weather.description}</p>
            <p>Temperature: {weather.temp}°F</p>
          </div>
        )}

        {recommendation && (
          <div className="bg-green-100 p-3 rounded border-l-4 border-green-500">
            <h2 className="font-semibold text-lg">LLM Says:</h2>
            <p>{recommendation}</p>
          </div>
        )}
      </div>
    </div>
  );
}
