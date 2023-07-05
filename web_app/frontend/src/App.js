import logo from './logo.svg';
import './App.css';
import Location from './components/Location';
import data from "./locationjunk"

console.log(data)



function App() {
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
      {locations}
    </div>
  );
}

export default App;
