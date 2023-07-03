import { NavLink, Route, Routes } from "react-router-dom";
import { useLocation } from "react-router-dom";
import AdvancedSearch from "../../pages/AdvancedSearch";
import ListView from "../../pages/ListView";
import Contact from "../../pages/Contact";
import Menu from "./subcomponents/menu/Menu.jsx";
import Login from "../../pages/Login";
import "./NavigationCSS.css";

export default function Navigation() {
  const location = useLocation();
  return (
    <div className="nav-container">
      <div className="navigation-column">
        <Menu />
        <NavLink to="/login" className={location.pathname === "/login" ? "active-link" : ""}>
          <button type="button" className="btn btn-outline-light customMenu">Login</button>
        </NavLink>
      </div>
      <div className="navigation-column">
        <Routes>
          <Route path="/advancedsearch" element={<AdvancedSearch />} />
          <Route path="/listview" element={<ListView />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </div>
  );
}
