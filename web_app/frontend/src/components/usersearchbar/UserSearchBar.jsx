import React, {useState, useEffect} from "react";
import "./UserSearchBarCSS.css";
import WeatherComponent from "../weatherInfo/WeatherComponent";
import UserSearchMenu from "./UserSearchMenu";
import {
  getAllBusyness,
  filterBusyness,
} from "../busynessInfo/currentBusyness";
import ToggleViewButton from './ToggleViewButton'

export default function UserSearchBar({toggleViewMode, viewMode, onBusynessChange, zones, ...props}) {
  const [busynessLevel, setBusynessLevel] = useState(3);
  const [selectedZones, setSelectedZones] = useState();


  useEffect(() => {
    console.log("Zone change!")
    if (Object.keys(zones).length !== 0) {
      // check if zones is not an empty object
      const filteredZones = filterBusyness(busynessLevel, zones);
      // console.log("filteredZones:", filteredZones);
      props.setSelectedZones(filteredZones);
    }
  }, [busynessLevel, zones]);

  useEffect(() => {
    // console.log("selectedZones:", selectedZones);
  }, [selectedZones]);

  // change to current busyness on map if busyness changes
  useEffect(() => {
    onBusynessChange('heatmap');
  }, [busynessLevel]);

  const handleBusynessChange = (event) => {
    setBusynessLevel(Number(event.target.value)); // Convert value to number
    // console.log(`User selected busyness level: ${event.target.value}`);
  };

  return (
    <div className="usersearch-container">
      <div className="offcanvas-content">
        <div className="weather-time-reset-container">
          <ToggleViewButton
            isSearched={props.isSearched}
            viewMode={viewMode}
            toggleViewMode={toggleViewMode}
          />
          <div className="weather-time-container">
            <div className="weather-icon">
              <WeatherComponent/>
            </div>
            <div className="current-time">{getCurrentTime()}</div>
          </div>
        </div>
        <div className="label-container">
          <label htmlFor="busyness-slider" className="form-label" id="busyness-slider-label">
            busyness in Manhattan
          </label>
        </div>
        <div className="busyness-level">
          <input
            type="range"
            className="range-cust"
            min="1"
            max="5"
            id="busyness-slider"
            onChange={handleBusynessChange}
            value={busynessLevel}
          />
          <div className="scale-labels">
            <span>less busy</span>
            <span>more busy</span>
          </div>
        </div>
        <UserSearchMenu
          onSearch={props.onSearch}
          isSearched={props.isSearched}
          searchResults={props.searchResults}
        />
      </div>
      <div className="button-wrapper">
        <button
          className="btn btn-primary offcanvas-button"
          id="search-menu-open-button"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#offcanvasBottom"
          aria-controls="offcanvasBottom"
        >
          <svg
            id="search-menu-open-icon"
            viewBox="0 0 24 24"
            fill="#FFFFFF"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M18.2929 15.2893C18.6834 14.8988 18.6834 14.2656 18.2929 13.8751L13.4007 8.98766C12.6195 8.20726 11.3537 8.20757 10.5729 8.98835L5.68257 13.8787C5.29205 14.2692 5.29205 14.9024 5.68257 15.2929C6.0731 15.6835 6.70626 15.6835 7.09679 15.2929L11.2824 11.1073C11.673 10.7168 12.3061 10.7168 12.6966 11.1073L16.8787 15.2893C17.2692 15.6798 17.9024 15.6798 18.2929 15.2893Z"/>
          </svg>
        </button>
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
    month: "short",
  };
  const time = now.toLocaleTimeString("en-US", optionsTime);
  const date = now.toLocaleDateString("en-US", optionsDate);
  
  // Split the date string into day and month parts
  const [day, month] = date.split(" ");
  
  return `${month}/${day}`;
}

console.log(getCurrentTime());

