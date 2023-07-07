import Navigation from '../components/navigation/Navigation.jsx';
import { Logo } from "../components/logo/Logo";
import MapBackground from '../components/mapBackground/MapBackground.jsx';
import UserSearchBar from '../components/usersearchbar/UserSearchBar.jsx';
import "./homePageCSS.css"
import WeatherComponent from '../components/weatherInfo/WeatherComponent.jsx';
export default function Homepage() {
  return (
    <div className='app-container'>
      <MapBackground/>
      <div className='header-container'>
        <Logo/>
        <div className="side-naviagtion-container">
            <Navigation/>
        </div>
      </div>
      <div className="main-application-container">
        <div className="main-body-container">
          <WeatherComponent/>
        </div>
        <div className="main-footer-container">
          <UserSearchBar/>
        </div>
        
      </div>
    </div>
  )
}
