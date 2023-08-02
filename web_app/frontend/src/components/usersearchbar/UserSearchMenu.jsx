import React, { useState, useRef } from "react";
import TimeButton from "./TimeButton";
import TreeButton from "./TreeButton";
import BusynessButton from "./BusynessButton";
import StyleButton from "./StyleButton";
import SearchResult from "../searchresult/SearchResult";
import { handleSearch } from "../searchresult/SearchResult";
import "./UserSearchMenuCSS.css";
import "../searchresult/SearchResultCSS.css";
import moment from "moment-timezone";
import WeatherButton from "./WeatherButton";

export default function UserSearchMenu(props) {
  const [searchOptions, setSearchOptions] = useState({
    datetime: moment().tz("America/New_York").format("YYYY-MM-DD HH:mm"),
    busyness: 1,
    style: "neo-Georgian",
    tree: 1,
  });
  //const [searchResults, setSearchResults] = useState([]);
  //const [isSearched, setIsSearched] = useState(false);

  // Create a ref for the offcanvas
  const offCanvasRef = useRef(null);

  const handleOptionsChange = (optionName, optionValue) => {
    setSearchOptions({ ...searchOptions, [optionName]: optionValue });
  };

  const onSearch = async () => {
    const results = await handleSearch(searchOptions);
    props.onSearch(results, searchOptions)
    //setSearchResults(results);
    //setIsSearched(true);

    // Change the height of the offcanvas after search
    offCanvasRef.current.style.height = "60%";
  };

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
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        />
      </div>

      <div className="scroll-container">
        <div className="offcanvas-body small">
          <div className="button-container">
            <TimeButton onChange={handleOptionsChange} />
            <TreeButton onChange={handleOptionsChange} />
            <BusynessButton onChange={handleOptionsChange} />
            <StyleButton onChange={handleOptionsChange} />
            <WeatherButton onChange={handleOptionsChange} />
            <button type="button" className="btn btn-dark" onClick={onSearch}>
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
