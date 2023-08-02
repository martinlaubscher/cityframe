import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const weatherOptions = {
  1: 'All',
  2: 'Clear',
  3: 'Clouds',
  4: 'Drizzle',
  5: 'Fog',
  6: 'Haze',
  7: 'Mist',
  8: 'Rain',
  9: 'Smoke',
  10: 'Snow',
  11: 'Squall',
  12: 'Thunderstorm'  
};

const WeatherButton = ({ onChange }) => {
  const handleOptionChange = (event) => {
    const selectedWeather = weatherOptions[event.target.value];
    onChange("weather", selectedWeather);
  };

  return (
    <div>
      <div className="option-container">
        <div className="option-label">Weather</div>
        <div className="option-list">
          <select className="weather-select" onChange={handleOptionChange}>
            {Object.keys(weatherOptions).map((key) => (
              <option key={key} value={key}>
                {weatherOptions[key]}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default WeatherButton;
