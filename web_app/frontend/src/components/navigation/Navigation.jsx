import { NavLink, Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";
import AdvancedSearch from "../../pages/AdvancedSearch";
import ListView from "../../pages/ListView";
import Contact from "../../pages/Contact";
import Login from "../../pages/Login";
import "./NavigationCSS.css";

export default function Navigation_offcanvas() {
  const location = useLocation();
  return (
    <div className="nav-container">
      <button className="btn btn-dark menu-button" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasTop" aria-controls="offcanvasTop">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff"><g id="SVGRepo_bgCarrier" strokeWidth="0"></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fillRule="evenodd" clipRule="evenodd" d="M3 6C3 5.44772 3.44772 5 4 5H20C20.5523 5 21 5.44772 21 6C21 6.55228 20.5523 7 20 7H4C3.44772 7 3 6.55228 3 6ZM3 12C3 11.4477 3.44772 11 4 11H20C20.5523 11 21 11.4477 21 12C21 12.5523 20.5523 13 20 13H4C3.44772 13 3 12.5523 3 12ZM3 18C3 17.4477 3.44772 17 4 17H20C20.5523 17 21 17.4477 21 18C21 18.5523 20.5523 19 20 19H4C3.44772 19 3 18.5523 3 18Z" fill="#ffffff"></path> </g>
    </svg></button>
    
    <div className="offcanvas offcanvas-top" tabIndex="-1" id="offcanvasTop" aria-labelledby="offcanvasTopLabel">
      <div className="offcanvas-header text-bg-dark">
        <h5 className="offcanvas-title" id="offcanvasTopLabel">CITYFRAME</h5>
        <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div className="offcanvas-body text-bg-dark">
        <ul className="nav flex-column pe-5">
          <li className="nav-item ">
            <NavLink to="/login" className={location.pathname === "/login" ? "active-link" : ""}>Login</NavLink>
          </li>
          <li className="nav-item ">
            <NavLink to="/contact" className={location.pathname === "/contact" ? "active-link" : ""}>Contact</NavLink>
          </li>
          <li className="nav-item ">
            <NavLink to="/listview" className={location.pathname === "/listview" ? "active-link" : ""}>List View</NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/advancedsearch" className={location.pathname === "/advancedsearch" ? "active-link" : ""}>Advanced Search</NavLink>
          </li>
        </ul>

        <Routes>
          <Route path="/advancedsearch" element={<AdvancedSearch />} />
          <Route path="/listview" element={<ListView />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login />} />
        </Routes>

      </div>
    </div>
    </div>
  );
}
