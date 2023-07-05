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
      <button class="btn btn-dark menu-button" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasTop" aria-controls="offcanvasTop"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
      <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/>
    </svg></button>
    
    <div class="offcanvas offcanvas-top" tabindex="-1" id="offcanvasTop" aria-labelledby="offcanvasTopLabel">
      <div class="offcanvas-header text-bg-dark">
        <h5 class="offcanvas-title" id="offcanvasTopLabel">CITYFRAME</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body text-bg-dark">
        <ul class="nav flex-column pe-5">
          <li class="nav-item ">
            <NavLink to="/login" className={location.pathname === "/login" ? "active-link" : ""}>Login</NavLink>
          <li class="nav-item ">
            <NavLink to="/contact" className={location.pathname === "/contact" ? "active-link" : ""}>Contact</NavLink>
          </li>
            <NavLink to="/listview" className={location.pathname === "/listview" ? "active-link" : ""}>List View</NavLink>
          </li>
          <li class="nav-item">
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
