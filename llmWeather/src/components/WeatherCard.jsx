import { useRef, useEffect } from 'react';

export default function WeatherCard() {
  const dateTimeRef = useRef(null);

  useEffect(() => {
    // Date/time updater
    function updateDateTime() {
      const now = new Date();
      const optionsDate = { weekday: "long" };
      const optionsTime = { hour: "2-digit", minute: "2-digit", hour12: false };
      if (dateTimeRef.current) {
        dateTimeRef.current.textContent = `${now.toLocaleDateString(undefined, optionsDate)}, ${now.toLocaleTimeString([], optionsTime)}`;
      }
    }
    updateDateTime();
    const interval = setInterval(updateDateTime, 60000);
    // Cleanup
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="w-full max-w-lg mx-auto p-4 bg-white rounded shadow relative">
      <div ref={dateTimeRef} className="text-center text-gray-700 text-sm mb-2" />
    </div>
  );
}