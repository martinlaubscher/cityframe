import CFlogo from '../../assets/SWcityframe.png';
import otherlogo from '../../assets/CFlogo.png';
import Bcityframe from "../../assets/Bcityframe.png"
import './LogoCSS.css';

export function Logo() {
  return (
    <div className="logo-container">
      <img className="logo-image" src={Bcityframe} alt="CFlogo" />
    </div>
  );
}