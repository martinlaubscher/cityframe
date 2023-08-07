import CFlogo from "../../assets/SWcityframe.png";
import CFlogo_avif from "../../assets/SWcityframe.avif";

import "./LogoCSS.css";

export function Logo() {
  return (
    <div className="logo-container">
      <picture>
        <source className="logo-image" srcSet={CFlogo_avif} type="image/avif" />
        <img className="logo-image" src={CFlogo} alt="CFlogo" />
      </picture>
    </div>
  );
}
