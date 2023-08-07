import React, {useState, useRef, useEffect} from "react";
import TimeButton from "./TimeButton";
import TreeButton from "./TreeButton";
import BusynessButton from "./BusynessButton";
import StyleButton from "./StyleButton";
import TypeButton from "./TypeButton";
import SearchResult from "../searchresult/SearchResult";
import {handleSearch} from "../searchresult/SearchResult";
import "./UserSearchMenuCSS.css";
import "../searchresult/SearchResultCSS.css";
import moment from "moment-timezone";
import WeatherButton from "./WeatherButton";
import ClearSearchButton from './ClearSearchButton';

export default function UserSearchMenu(props) {
  const [searchOptions, setSearchOptions] = useState({
    datetime: moment().tz("America/New_York").format("YYYY-MM-DD HH:mm"),
    busyness: 1,
    style: "neo-Georgian",
    zone_type: "Commercial",
    tree: 1,
    weather: "All"
  });
  const [searchResults, setSearchResults] = useState([]);
  const [isSearched, setIsSearched] = useState(false);
  const [clear, setClear] = useState(false);

  // Create a ref for the offcanvas
  const offCanvasRef = useRef(null);

  const handleOptionsChange = (optionName, optionValue) => {
    setSearchOptions({...searchOptions, [optionName]: optionValue});
  };

  const onSearch = async () => {
    const results = await handleSearch(searchOptions);
    props.onSearch(results, searchOptions)
    //setSearchResults(results);
    //setIsSearched(true);

    // Change the height of the offcanvas after search
    offCanvasRef.current.style.height = "60%";
  };

  const clearSearchOptions = () => {
    setSearchOptions({
      datetime: moment().tz("America/New_York").format("YYYY-MM-DD HH:mm"),
      busyness: 1,
      style: "neo-Georgian",
      zone_type: "Commercial",
      tree: 1,
      weather: "All"
    });
    setSearchResults([]);
    setIsSearched(false);
    console.log('search cleared')
    setClear(true); // set clear flag
  };

  useEffect(() => {
    if (clear) setClear(false);
  }, [clear]);

  return (
    <div
      ref={offCanvasRef}
      className="offcanvas offcanvas-bottom"
      tabIndex="-1"
      id="offcanvasBottom"
      aria-labelledby="offcanvasBottomLabel"
    >
      <div className="button-wrapper-close">
        <button
          type="button"
          className="btn-close"
          id="search-menu-close-button"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        />
      </div>

      <div className="scroll-container">
        <div className="offcanvas-body small">
          <div className="search-description-container">
            <p className="search-description">search the city zones</p>
            <p className="search-explanation">find locations according to the following parameters</p>
          </div>
          <div className="clear-search-container">
            <ClearSearchButton clearSearchOptions={clearSearchOptions}/>
          </div>
          <div className="button-container">
            <TimeButton onChange={handleOptionsChange} clear={clear}/>
            <TreeButton onChange={handleOptionsChange} clear={clear}/>
            <BusynessButton onChange={handleOptionsChange} clear={clear}/>
            <StyleButton onChange={handleOptionsChange} clear={clear}/>
            <TypeButton onChange={handleOptionsChange} clear={clear}/>
            <WeatherButton onChange={handleOptionsChange} clear={clear}/>
            <button type="button" className="btn search-button" id="search-button" onClick={onSearch}>
              Search
            </button>
          </div>
        </div>
        <div className="result-container">
          {props.isSearched && <SearchResult results={props.searchResults} searchOptions={searchOptions}/>
          }
        </div>
      </div>
    </div>
  );
}
