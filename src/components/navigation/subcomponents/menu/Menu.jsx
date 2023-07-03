import { useLocation } from "react-router-dom";
import { NavLink } from "react-router-dom";
import "../../NavigationCSS.css";

export default function Menu() {
  const location = useLocation();

  return (
    <div>
      <div className="dropup-center dropend">
        <button className="btn btn-outline-light dropdown-toggle customMenu" type="button" data-bs-toggle="dropdown" aria-expanded="false">
          Menu
        </button>
        <ul className="dropdown-menu">
        <li>
        <NavLink to="/contact" className={location.pathname === "/contact" ? "active-link" : ""}>Contact</NavLink>
        </li>
        <li>
        <NavLink to="/listview" className={location.pathname === "/listview" ? "active-link" : ""}>List View</NavLink>
        
        </li>
        <li>
        <NavLink to="/advancedsearch" className={location.pathname === "/advancedsearch" ? "active-link" : ""}>AdvancedSearch</NavLink>
        
        </li>
        
        </ul>
      </div>
    </div>
  );
}
