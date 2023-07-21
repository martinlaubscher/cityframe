import Navigation from '../components/navigation/Navigation.jsx';
import { Logo } from "../components/logo/Logo";
import MapBackground from '../components/mapBackground/MapBackground.jsx';
import UserSearchBar from '../components/usersearchbar/UserSearchBar.jsx';
import "./homePageCSS.css"
import WeatherComponent from '../components/weatherInfo/WeatherComponent.jsx';

import Map from '../components/mapBackground/Map.jsx';
import dynamic from '../components/dummydata/geojunk.js';
import data from '../components/dummydata/locationjunk.js';
import { useState, useEffect } from 'react';
import Droplist from '../components/droplist/Droplist.jsx';
//import mandata from '../components/data/manhattan_taxi_zones.geojson';

export default function Homepage() {
  //console.log(mandata)
  
  const [listResults, setListResults]=useState({results: dynamic, name: "All Zones"})
  const [listShow, setListShow]=useState(false)
  const [scores, setScores]=useState([5])
  
  function searchFilter(){
    //Take in dictionary of all places and times in search (I think??) and all parameters
    const allIds = dynamic.map(place=>{return place.id})
    console.log("All ids", allIds)
    const search={places: allIds, times: [1, 2], params: {busyness: 50}}
    
    const places=dynamic.filter(item => search.places.includes(item.id))
    console.log("places", places)

    const items=places.map(item=> {
      return {id:item.id, data:item.data.filter(datum => search.times.includes(datum.time))}
    })
    console.log("items", items)

    calculateScores(items, search.params)
  }

  function calculateScores(items, params){
    console.log("About to set score using", items)
    setScores(items.map(item=>{
      console.log("Set score now", item)
      return {id: item.id, data: item.data.map(time=>{
        const score=100-Math.abs(time.busyness-params.busyness)
        return {time: time.time, score: score}
      }
      )}
    }))
    console.log("Score:", scores)
  }

  function buildlist(results){
    const items=dynamic.filter(item => item.id===results.properties.location_id)
    console.log(scores)
    const placeScores=scores.filter(item => item.id===results.properties.location_id)
    console.log(placeScores)
    setListResults({items: items, name: results.properties.zone, score: placeScores})
    setListShow(true)
    }
  
  function hideList(){
    setListShow(false)    
  }
  useEffect(function() {
        searchFilter()
  }, [])//put the search thing in the dependancies array


  return (
    <div className='app-container'>
      <div className='header-container'>
        <Logo/>
        <div className="side-naviagtion-container">
            <Navigation/>
        </div>
      </div>
      <div className="main-application-container">
        <div className="main-body-container">
          {/* <WeatherComponent/> */}
          <Map
            data={data}
            buildlist={buildlist}
            />
        </div>
        <div className="main-footer-container">
          <UserSearchBar/>
        </div>
        {listShow && <Droplist results={listResults} hideList={hideList}/>}
        
      </div>
    </div>
  )
}
