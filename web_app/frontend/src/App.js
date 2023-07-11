import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import Location from './components/Location';
import Map from './components/Map';
import Droplist from './components/Droplist';
import data from "./locationjunk"
import dynamic from './dynamicjunk'
import { Dropdown } from 'bootstrap';





function App() {
  //const [searchResults, setSearchResults]=useState(dynamic)
  const [listResults, setListResults]=useState(dynamic)
  function buildlist(results){
    const items=dynamic.filter(item => item.id===results.id)
    setListResults(items)
    }


  const locations=data.map(loc =>{
    return(
      <Location
      key={loc.id}
      name={loc.name}
      coordinates={loc.coordinates} 
      />)
  })


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <Droplist 
      results={listResults}
      />
      {locations}
      <Map 
      data={data}
      buildlist={buildlist}
      />
    </div>
  );
}

export default App;
