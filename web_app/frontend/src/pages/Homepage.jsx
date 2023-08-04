import Navigation from "../components/navigation/Navigation.jsx";
import { Logo } from "../components/logo/Logo";
//import MapBackground from '../components/mapBackground/MapBackground.jsx';
import UserSearchBar from "../components/usersearchbar/UserSearchBar.jsx";
import "./homePageCSS.css";

import Map from "../components/mapBackground/Map.jsx";
import junkdynamic from "../components/dummydata/geojunk.js";
import dynamic from "../components/dummydata/dynamicdata.js";
import data from "../components/dummydata/locationjunk.js";
import { useState, useEffect } from "react";
import Droplist from "../components/placeList/Droplist.jsx";
import colours from '../components/dummydata/colours.js';

export default function Homepage() {
  //console.log(dynamic)
  const [selectedZones, setSelectedZones] = useState();
  
  const [listResults, setListResults] = useState({
    results: junkdynamic,
    name: "All Zones",
  });
  const [listShow, setListShow] = useState(false);
  const [scores, setScores] = useState({});

  const [searchResults, setSearchResults] = useState([]);
  const [isSearched, setIsSearched] = useState(false);
  const [searchOptions, setSearchOptions] = useState();

  // state variable to keep track of what is shown on map
  const [viewMode, setViewMode] = useState('heatmap');

  function onSearch (results, options){
    results = results.map(result => {
      var resultColour = colours.find(colour => colour.location_id === result.id);
      // var resultImgURL = ImgURL.find(img => img.location_id === result.id);
      return {
        ...result,  
        pallete: resultColour?.colors, // fix undifined situation
        // imageUrl: resultImgURL?.image_url // fix undifined situation
      }
    });

    setSearchOptions(options);
    setSearchResults(results);
    setIsSearched(true);

    // set view mode to 'results' after a search
    setViewMode('results');
  }
  function buildlist(feature, rank) {

    setListResults({ place: feature, rank: rank });
    setListShow(true);
  }

  function hideList() {
    setListShow(false);
  }

  function toggleViewMode() {
    setViewMode(viewMode === 'heatmap' ? 'results' : 'heatmap');
    console.log(viewMode)
  }

  return (
    <div className='app-container'>
      <div className='header-container'>
        <Logo/>
        {/*<div className="side-naviagtion-container">*/}
        <Navigation/>
        {/*</div>*/}
      </div>
      <div className="main-application-container">
        <div className="main-body-container">
          <Map
            data={data}
            scores={scores}
            buildlist={buildlist}
            isSearched={isSearched}
            searchResults={searchResults}
            busynessZones={selectedZones}
            viewMode={viewMode}
          />
        </div>

        <div className="main-footer-container">
          <UserSearchBar
            onSearch={onSearch}
            isSearched={isSearched}
            searchResults={searchResults}
            setSelectedZones={setSelectedZones} 
            selectedZones={selectedZones}
            toggleViewMode={toggleViewMode}
            viewMode={viewMode}
          />
        </div>
        {listShow && (
          <Droplist
            results={listResults}
            searchOptions={searchOptions}
            hideList={hideList}
          />
        )}


      </div>
    </div>
  );
}
