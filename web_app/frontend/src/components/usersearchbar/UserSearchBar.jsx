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
    // console.log("Zone change!")
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
            busyness in manhattan
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
          <svg width="256px" height="256px" viewBox="0 0 22 22" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000">

            <g id="SVGRepo_bgCarrier" stroke-width="0"/>

            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#CCCCCC" stroke-width="0.288"/>

            <g id="SVGRepo_iconCarrier">   <g id="🔍-Product-Icons" stroke-width="0.00024000000000000003" fill="none" fill-rule="evenodd"> <g id="ic_fluent_search_square_24_regular" fill="#ffffff" fill-rule="nonzero"> <path d="M17.75,3 C19.5449254,3 21,4.45507456 21,6.25 L21,6.25 L21,17.75 C21,19.5449254 19.5449254,21 17.75,21 L17.75,21 L6.25,21 C4.45507456,21 3,19.5449254 3,17.75 L3,17.75 L3,6.25 C3,4.45507456 4.45507456,3 6.25,3 L6.25,3 L17.75,3 Z M17.75,4.5 L6.25,4.5 C5.28350169,4.5 4.5,5.28350169 4.5,6.25 L4.5,6.25 L4.5,17.75 C4.5,18.7164983 5.28350169,19.5 6.25,19.5 L6.25,19.5 L17.75,19.5 C18.7164983,19.5 19.5,18.7164983 19.5,17.75 L19.5,17.75 L19.5,6.25 C19.5,5.28350169 18.7164983,4.5 17.75,4.5 L17.75,4.5 Z M11,7.25 C13.0710678,7.25 14.75,8.92893219 14.75,11 C14.75,11.7642046 14.5214065,12.4750184 14.1288677,13.0677932 L16.5303301,15.4696699 C16.8232233,15.7625631 16.8232233,16.2374369 16.5303301,16.5303301 C16.2640635,16.7965966 15.8473998,16.8208027 15.5537883,16.6029482 L15.4696699,16.5303301 L13.0677932,14.1288677 C12.4750184,14.5214065 11.7642046,14.75 11,14.75 C8.92893219,14.75 7.25,13.0710678 7.25,11 C7.25,8.92893219 8.92893219,7.25 11,7.25 Z M11,8.75 C9.75735931,8.75 8.75,9.75735931 8.75,11 C8.75,12.2426407 9.75735931,13.25 11,13.25 C12.2426407,13.25 13.25,12.2426407 13.25,11 C13.25,9.75735931 12.2426407,8.75 11,8.75 Z"> </path> </g> </g> </g>

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
  const [day, month] = date.split(" ");
  
  return `${time} ${month}/${day}`;
}