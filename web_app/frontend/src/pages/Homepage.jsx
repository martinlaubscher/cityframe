import Navigation from '../components/navigation/Navigation.jsx';
import { Logo } from "../components/logo/Logo";
//import MapBackground from '../components/mapBackground/MapBackground.jsx';
import UserSearchBar from '../components/usersearchbar/UserSearchBar.jsx';
import "./homePageCSS.css"



import Map from '../components/mapBackground/Map.jsx';
import junkdynamic from '../components/dummydata/geojunk.js';
import dynamic from '../components/dummydata/dynamicdata.js';
import data from '../components/dummydata/locationjunk.js';
import { useState, useEffect } from 'react';
import Droplist from '../components/placeList/Droplist.jsx';
import SearchResult from '../components/searchresult/SearchResult.jsx';
//import mandata from '../components/data/manhattan_taxi_zones.geojson';

export default function Homepage() {

  const [listResults, setListResults]=useState({})
  const [listShow, setListShow]=useState(false)
  const [scores, setScores]=useState({})
  

  const [searchResults, setSearchResults] = useState([]);
  const [isSearched, setIsSearched] = useState(false);
  const [searchOptions, setSearchOptions] = useState();

  function onSearch (results, options){
    setSearchOptions(options)
    setSearchResults(results);
    setIsSearched(true);
  }


    /*
  function searchFilter(){
    //Take in dictionary of all places and times in search (I think??) and all parameters
    //const allIds = junkdynamic.map(place=>{return place.id})
    const someIds = Object.keys(dynamic)
    //const search={places: allIds, times: [1, 2], params: {busyness: 0}}
    const search={places: someIds, params: {busyness : 5, trees: 5, style: "default"}}
    
    //const places=junkdynamic.filter(item => search.places.includes(item.id))
    const items={...dynamic}

    for (let key in dynamic){
      if (!search.places.includes(key)){
        delete items[key]
      }
    }


    //const items=places.map(item=> {
    //  return {id:item.id, data:item.data.filter(datum => search.times.includes(datum.time))}
    //})

    calculateScores(items, search.params)
  }


  function calculateScores(items, params){
    var tempScores={}
    for (let key in items){
      var score=100-Math.round((Math.abs(items[key].busyness-params.busyness)+Math.abs(items[key].trees-params.trees)+(params.style===items[key].style ? 0 : 5))*20/3)
      var time=items[key].dt_iso
      tempScores[key]={score: score, time: time}
    }
    setScores(tempScores)

    setScores( 
      items.map(item=>{
      return {id: item.id, data: item.data.map(time=>{
        const score=100-Math.abs(time.busyness-params.busyness)
        return {time: time.time, score: score}
      }
      )}
    }))
  }
  */

  function buildlist(feature, rank){
    //const items=junkdynamic.filter(item => item.id===results.properties.location_id)
    //setListResults({items: items, name: results.properties.zone, score: placeScore})
    
    setListResults({place: feature, rank: rank})
    setListShow(true)
    }
  
  function hideList(){
    setListShow(false)    
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
          {/* <WeatherComponent/> */}
          <Map
            data={data}
            scores={scores}
            buildlist={buildlist}
            isSearched={isSearched}
            searchResults={searchResults}
            />
        </div>
        {/*
        <div className="main-footer-container">
          <UserSearchBar onSearch={onSearch} isSearched={isSearched} searchResults={searchResults}/>
        </div>
        {listShow && <Droplist results={listResults} searchOptions={searchOptions} hideList={hideList}/>}
        {//listShow && <div className="result-container">
          //{<SearchResult results={searchResults} searchOptions={searchOptions} onePlace={true}/>}
        //</div>
      }*/}


      </div>
    </div>
  )
}
