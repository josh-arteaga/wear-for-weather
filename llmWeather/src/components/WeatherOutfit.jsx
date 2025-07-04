// src/components/WeatherOutfit.jsx
import { useState } from 'react';
import { useCoords } from '../hooks/useCoords';

export default function WeatherOutfit() {
  const coords = useCoords();
  const [loading, setLoading] = useState(false);
  const [weather, setWeather] = useState(null);
  const [recommendation, setRecommendation] = useState('');

  const handleGetRecommendation = async () => {
    if (!coords) return;
    const { lat, lon } = coords;
    setLoading(true);
    setWeather(null);
    setRecommendation('');
    try {
      const weatherRes = await fetch(`http://127.0.0.1:8000/weather?lat=${lat}&lon=${lon}`);
      if (!weatherRes.ok) throw new Error(`Weather fetch ${weatherRes.status}`);
      const weatherData = await weatherRes.json();
      setWeather(weatherData);
      console.log('Weather data:', weatherData);

      const recRes = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(weatherData),
      });
      if (!recRes.ok) throw new Error('LLM fetch ${recRes.status}');
      setRecommendation(await recRes.text());
    } catch (err) {
      console.error('Fetch error:', err);
      setRecommendation('⚠️ Something blew up – check console.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-md mt-10">
      <h1 className="text-2xl font-bold mb-4 text-center">What Should I Wear?</h1>
      <div className="mb-4 text-center">
        {coords ? (
        (() => {
          console.log(`Using your location: lat ${coords.lat.toFixed(4)}, lon ${coords.lon.toFixed(4)}`);
          return null;
        })()
        ) : (
          <span className="text-sm text-gray-400">Getting your location…</span>
        )}
      </div>
      <button
        onClick={handleGetRecommendation}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        disabled={loading || !coords}
      >
        {loading ? 'Thinking…' : 'Get Recommendation'}
      </button>
      <div className="mt-6 space-y-4">
        {weather && (
          <div className="bg-gray-100 p-3 rounded">
            <h2 className="font-semibold text-lg">Weather</h2>
            <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(weather, null, 2)}</pre>
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
