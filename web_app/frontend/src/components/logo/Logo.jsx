import CFlogo from '../../assets/CFlogo.png';
import './LogoCSS.css';

export function Logo() {
  return (
    <div className="logo-container">
      <img className="logo-image" src={CFlogo} alt="CFlogo" />
    </div>
  );
}