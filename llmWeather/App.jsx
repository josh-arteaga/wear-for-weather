import React, { useState, useEffect } from "react";
import WeatherOutfit from "./src/components/WeatherOutfit";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  return (
    <div>
      <button
        onClick={() => setDarkMode((d) => !d)}
        className="absolute top-4 right-4 text-sm underline"
      >
        {darkMode ? "Light" : "Dark"} mode
      </button>
      <WeatherOutfit />
    </div>
  );
}