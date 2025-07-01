import { useEffect, useState } from "react";

export function useCoords() {
  const [coords, setCoords] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => setCoords({ lat: coords.latitude, lon: coords.longitude }),
      (err) => {
        console.warn("Geolocation error:", err);
        setCoords({ lat: 30.2672, lon: -97.7431 }); // Austin fallback
      }
    );
  }, []);

  return coords;
}
