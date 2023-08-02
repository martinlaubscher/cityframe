import React, { useState, useEffect } from "react";
import "./UserSearchBarCSS.css";
import WeatherComponent from "../weatherInfo/WeatherComponent";
import UserSearchMenu from "./UserSearchMenu";
import {
  getAllBusyness,
  filterBusyness,
} from "../busynessInfo/currentBusyness";

export default function UserSearchBar(props) {
  const [busynessLevel, setBusynessLevel] = useState(3);
  const [zones, setZones] = useState({});
  const [selectedZones, setSelectedZones] = useState();

  // Get data from API when component mounts
  useEffect(() => {
    getAllBusyness()
      .then((data) => {
        // Ensure that data is an object before setting zones
        if (data && typeof data === 'object') {
          setZones(data);
        } else {
          // If data is not an object, set zones as an empty object
          setZones({});
        }
      })
      .catch((error) => {
        console.error('Error fetching busyness data:', error);
        // If there's an error, set zones as an empty object
        setZones({});
      });
  }, []);


  useEffect(() => {
    if (Object.keys(zones).length !== 0) {
      // check if zones is not an empty object
      const filteredZones = filterBusyness(busynessLevel, zones);
      console.log("filteredZones:", filteredZones);
      props.setSelectedZones(filteredZones);
    }
  }, [busynessLevel, zones]);

  useEffect(() => {
    console.log("selectedZones:", selectedZones);
  }, [selectedZones]);

  const handleBusynessChange = (event) => {
    setBusynessLevel(Number(event.target.value)); // Convert value to number
    console.log(`User selected busyness level: ${event.target.value}`);
  };

  return (
    <div className="usersearch-container">
      <div className="button-wrapper">
        <button
          className="btn btn-primary offcanvas-button"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#offcanvasBottom"
          aria-controls="offcanvasBottom"
        >
          <svg
            viewBox="0 0 24 24"
            fill="#FFFFFF"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M18.2929 15.2893C18.6834 14.8988 18.6834 14.2656 18.2929 13.8751L13.4007 8.98766C12.6195 8.20726 11.3537 8.20757 10.5729 8.98835L5.68257 13.8787C5.29205 14.2692 5.29205 14.9024 5.68257 15.2929C6.0731 15.6835 6.70626 15.6835 7.09679 15.2929L11.2824 11.1073C11.673 10.7168 12.3061 10.7168 12.6966 11.1073L16.8787 15.2893C17.2692 15.6798 17.9024 15.6798 18.2929 15.2893Z" />
          </svg>
        </button>
      </div>

      <div className="offcanvas-content">
        <div className="weather-icon-container">
          <div className="label-container">
            <label htmlFor="customRange2" className="form-label">
              Busyness
            </label>
          </div>
          <div className="weather-icon">
            <WeatherComponent />
          </div>
          <div className="current-time">{getCurrentTime()}</div>
        </div>
        <div className="busyness-level">
          <input
            type="range"
            className="form-range range-cust"
            min="1"
            max="5"
            id="customRange2"
            onChange={handleBusynessChange}
            value={busynessLevel}
          />
        </div>
        <UserSearchMenu
          onSearch={props.onSearch}
          isSearched={props.isSearched}
          searchResults={props.searchResults}
        />
      </div>
    </div>
  );
}

function getCurrentTime() {
  const now = new Date();
  const optionsTime = {
    timeZone: "America/New_York",
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
  };
  const optionsDate = {
    timeZone: "America/New_York",
    day: "2-digit",
    month: "2-digit",
  };
  const time = now.toLocaleTimeString("en-US", optionsTime);
  const date = now.toLocaleDateString("en-US", optionsDate);
  return `${time} ${date}`;
}
