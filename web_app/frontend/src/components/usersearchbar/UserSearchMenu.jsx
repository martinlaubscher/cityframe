import React, { useState, useEffect } from "react";
import TimeButton from "./TimeButton";
import TreeButton from "./TreeButton";
import BusynessButton from "./BusynessButton";
import StyleButton from "./StyleButton";
import SearchResult from "../searchresult/SearchResult";
import { handleSearch } from "../searchresult/SearchResult";
import { fetchFakeSearchResults } from "../searchresult/fakeSearchResults";
import "./UserSearchMenuCSS.css";
import "../searchresult/SearchResultCSS.css";


export default function UserSearchMenu() {
  const [searchOptions, setSearchOptions] = useState({
    datetime: new Date(),
    busyness: 1,
    style: "Beaux-Arts",
    tree: false,
  });
  const [searchResults, setSearchResults] = useState([]);

  const handleOptionsChange = (optionName, optionValue) => {
    console.log(
      "UserSearchMenu optionName:",
      optionName,
      "optionValue:",
      optionValue
    ); // Log optionName and optionValue
    setSearchOptions({ ...searchOptions, [optionName]: optionValue });
  };
  // ------------Notice：uncomment below code in final version---------------------

  const onSearch = async () => {
    const results = await handleSearch(searchOptions);
    setSearchResults(results);
  };

  // fake input
  // {
  //   "time": "2023-07-31 08:35",
  //   "busyness": 3,
  //   "trees": 1,
  //   "style": "Beaux-Arts"
  // } '
  // -------------------junk data code(without api)--------------------------------
  // const onSearch = async () => {
  //   try {
  //     const results = await fetchFakeSearchResults();
  //     setSearchResults(Object.values(results));
  //   } catch (error) {
  //     console.error("Error fetching fake search results:", error);
  //     setSearchResults([]);
  //   }
  // };

  return (
    <div
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

      <div className="offcanvas-body small">
        <div className="button-container">
          <TimeButton onChange={handleOptionsChange} />
          <TreeButton onChange={handleOptionsChange} />
          <BusynessButton onChange={handleOptionsChange} />
          <StyleButton onChange={handleOptionsChange} />
          <button type="button" className="btn btn-dark" onClick={onSearch}>
            Search
          </button>
        </div>
      </div>
      <div className="result-container">
        <SearchResult results={searchResults} />
      </div>
    </div>
  );
}



