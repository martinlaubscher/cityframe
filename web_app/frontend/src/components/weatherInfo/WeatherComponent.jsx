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

const iconMapping = {
  "01d": faSun,
  "01n": faMoon,
  "02d": faCloudSun,
  "02n": faCloudMoon,
  "03d": faCloud,
  "03n": faCloud,
  "04d": faCloud,
  "04n": faCloud,
  "09d": faCloudShowersHeavy,
  "09n": faCloudShowersHeavy,
  "10d": faCloudSunRain,
  "10n": faCloudMoonRain,
  "11d": faBolt,
  "11n": faBolt,
  "13d": faSnowflake,
  "13n": faSnowflake,
  "50d": faSmog,
  "50n": faSmog
};

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
        <FontAwesomeIcon 
          icon={iconMapping[weather.weather[0].icon]} 
          className="weather-icon" 
          onClick={() => handleClick(weather.weather[0].description)}
        />
        {weatherDescription && <div className="weather-description-popup">{weatherDescription}</div>}
      </div>
    ) : (
      <div>Loading...</div>
    );
}

export default WeatherComponent;
