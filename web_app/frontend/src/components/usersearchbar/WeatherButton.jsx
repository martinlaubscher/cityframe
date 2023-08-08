import "./UserSearchMenuCSS.css";
import React, {useEffect, useState} from "react";

const weatherOptions = {
  1: 'all',
  2: 'clear',
  3: 'clouds',
  4: 'drizzle',
  5: 'fog',
  6: 'haze',
  7: 'mist',
  8: 'rain',
  9: 'smoke',
  10: 'snow',
  11: 'squall',
  12: 'thunderstorm'
};

const WeatherButton = ({onChange, clear}) => {

  const [selectedWeatherKey, setSelectedWeatherKey] = useState("1");

  const handleOptionChange = (event) => {
    const selectedKey = event.target.value;
    setSelectedWeatherKey(selectedKey);
    const selectedWeather = weatherOptions[selectedKey];
    onChange("weather", selectedWeather);
  };

  useEffect(() => {
    if (clear) {
      // reset to default key
      setSelectedWeatherKey("1");
      // notify parent of change
      onChange("weather", weatherOptions["1"]);
    }
  }, [clear, onChange]);

  return (
    <div>
      <div className="option-container">
        <div className="label-explanation-container">
          <div className="option-label">weather</div>
          <div className="option-explanation">
            preferred weather conditions
          </div>
        </div>
        <div className="option-list" id="weather-selection">
          <select className="weather-select" onChange={handleOptionChange} value={selectedWeatherKey}>
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
