import "./UserSearchMenuCSS.css";
import React, {useEffect, useState} from "react";

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
          <div className="option-label">Weather</div>
          <div className="option-explanation">
            {/*fill in as needed*/}
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
