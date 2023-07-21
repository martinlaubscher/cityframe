import React, { useState } from "react";
import TimeButton from "./TimeButton";
import TreeButton from "./TreeButton";
import BusynessButton from "./BusynessButton";
import StyleButton from "./StyleButton";
import SearchResult from "../searchresult/SearchResult";

export default function UserSearchMenu() {
  const [searchOptions, setSearchOptions] = useState({
    datetime: new Date(),
    busyness: 1,
    style: 1,
    tree: false,
  });
  const [searchResults, setSearchResults] = useState([]);

  const handleOptionsChange = (optionName, optionValue) => {
    setSearchOptions({ ...searchOptions, [optionName]: optionValue });
  };

  //--------------------------------------------test data------------------------⬇️
  const mockData = [
    { name: "Location1", datetime: "19", busyness: 2, style: 1, tree: false },
    { name: "Location2", datetime: new Date(), busyness: 1, style: 2, tree: true },
    { name: "Location3", datetime: new Date(), busyness: 3, style: 1, tree: false },
    { name: "Location4", datetime: new Date(), busyness: 4, style: 3, tree: true },
    // more data
  ];
  
  const handleSearch = () => {
    const results = mockData.filter(item => 
      item.busyness === searchOptions.busyness &&
      item.style === searchOptions.style &&
      item.tree === searchOptions.tree &&
      
      item.datetime.toDateString() === searchOptions.datetime.toDateString()
    );
    setSearchResults(results);
  };
  //--------------------------------------------test code------------------------⬆️

  // -------------------------change below code to call api-------------------------
  // const handleSearch = () => {
  //   // search logic
  //   const results = /* your search logic here */;
  //   setSearchResults(results);
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

          <button type="button" className="btn btn-dark" onClick={handleSearch}>Search</button>
          
          <SearchResult results={searchResults} />
        </div>
      </div>
    </div>
  );
}
