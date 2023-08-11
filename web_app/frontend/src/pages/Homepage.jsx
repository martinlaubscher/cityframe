import Navigation from "../components/navigation/Navigation.jsx";
import {Logo} from "../components/logo/Logo";
import UserSearchBar from "../components/usersearchbar/UserSearchBar.jsx";
import "./homePageCSS.css";

import Map from "../components/mapBackground/Map.jsx";
import junkdynamic from "../components/dummydata/geojunk.js";
import data from "../components/dummydata/locationjunk.js";
import {useState, useEffect} from "react";
import Droplist from "../components/placeList/Droplist.jsx";
import colours from '../components/dummydata/colours.js';
import {getAllBusyness} from "@/components/busynessInfo/currentBusyness.jsx";

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

  const handleBusynessChange = (value) => {
    // Your logic here
    setViewMode('heatmap');
  };

  function onSearch(results, options) {
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

    setListResults({place: feature, rank: rank});
    setListShow(true);
  }

  function hideList() {
    setListShow(false);
  }

  function toggleViewMode() {
    setViewMode(viewMode === 'heatmap' ? 'results' : 'heatmap');
    // console.log(viewMode)
  }

  const [zones, setZones] = useState({});

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


  return (
    <div className='app-container'>

      <div className='header-container'>

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
            zones={zones}
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
            onBusynessChange={handleBusynessChange}
            viewMode={viewMode}
            zones={zones}
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
