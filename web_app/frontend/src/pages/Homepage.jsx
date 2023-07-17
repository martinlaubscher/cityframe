import Navigation from '../components/navigation/Navigation.jsx';
import { Logo } from "../components/logo/Logo";
import MapBackground from '../components/mapBackground/MapBackground.jsx';
import UserSearchBar from '../components/usersearchbar/UserSearchBar.jsx';
import "./homePageCSS.css"
import WeatherComponent from '../components/weatherInfo/WeatherComponent.jsx';

import Map from '../components/mapBackground/Map.jsx';
import dynamic from '../components/dummydata/dynamicjunk.js';
import data from '../components/dummydata/locationjunk.js';
import { useState } from 'react';
import Droplist from '../components/Droplist/Droplist.jsx';

export default function Homepage() {
  
  const [listResults, setListResults]=useState(dynamic)
  const [listShow, setListShow]=useState(false)
  function buildlist(results){
    const items=dynamic.filter(item => item.id===results.id)
    setListResults(items)
    setListShow(true)
    }
  
  function hideList(){
    setListShow(false)    
  }


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
