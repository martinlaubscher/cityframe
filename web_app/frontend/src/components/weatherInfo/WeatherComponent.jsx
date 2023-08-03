import React, { useEffect, useState } from "react";
import axios from '@/axiosConfig';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSun,
  faMoon,
  faCloudSun,
  faCloudMoon,
  faCloud,
  faCloudShowersHeavy,
  faCloudSunRain,
  faCloudMoonRain,
  faBolt,
  faSnowflake,
  faSmog,
} from "@fortawesome/free-solid-svg-icons";
import "./WeatherInfoCSS.css";
function WeatherComponent() {

    const [weather, setWeather] = useState(null);
    const [weatherDescription, setWeatherDescription] = useState('');
  
    const handleClick = (description) => {
      if(weatherDescription === description) {
        setWeatherDescription('');
      } else {
        setWeatherDescription(description);
      }
    };
 
  useEffect(() => {
    axios
      .get("/api/current-weather/")

      .then((response) => {
        setWeather(response.data);
      })
      .catch((error) => {
        console.error("Error fetching weather data:", error);
      });
  }, []);

  return weather ? (
    <div className="weather-icon-container">
      {weather.weather[0].icon === "01d" && (
        <FontAwesomeIcon icon={faSun} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "01n" && (
        <FontAwesomeIcon icon={faMoon} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "02d" && (
        <FontAwesomeIcon icon={faCloudSun} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "02n" && (
        <FontAwesomeIcon icon={faCloudMoon} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "03d" && (
        <FontAwesomeIcon icon={faCloud} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "03n" && (
        <FontAwesomeIcon icon={faCloud} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "04d" && (
        <FontAwesomeIcon icon={faCloud} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "04n" && (
        <FontAwesomeIcon icon={faCloud} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "09d" && (
        <FontAwesomeIcon icon={faCloudShowersHeavy} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "09n" && (
        <FontAwesomeIcon icon={faCloudShowersHeavy} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "10d" && (
        <FontAwesomeIcon icon={faCloudSunRain} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "10n" && (
        <FontAwesomeIcon icon={faCloudMoonRain} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "11d" && (
        <FontAwesomeIcon icon={faBolt} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "11n" && (
        <FontAwesomeIcon icon={faBolt} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "13d" && (
        <FontAwesomeIcon icon={faSnowflake} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "13n" && (
        <FontAwesomeIcon icon={faSnowflake} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "50d" && (
        <FontAwesomeIcon icon={faSmog} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weather.weather[0].icon === "50n" && (
        <FontAwesomeIcon icon={faSmog} className="weather-icon" onClick={() => handleClick(weather.weather[0].description)} />
      )}
      {weatherDescription && <div className="weather-description-popup">{weatherDescription}</div>}
    </div>
  ) : (
    <div>Loading...</div>
  );
}

export default WeatherComponent;