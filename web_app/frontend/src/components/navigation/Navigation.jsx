import { NavLink, Route, Routes,useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import Contact from "../../pages/Contact";
import "./NavigationCSS.css";
import MostUniqueAreas from "../../pages/MostUniqueAreas";
import AboutThisWeb from "../../pages/AboutThisWeb";
import React, {useEffect, useState} from 'react';
import axios from "@/axiosConfig.js";
import colours from '../dummydata/colours.js';


export default function Navigation_offcanvas() {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedNavItem, setSelectedNavItem] = useState(null); // add this line
  const [gemResults, setGemResults] = useState([null]);
  const [zoneIDs, setZoneIDs] = useState([null]);
  const [showExtraSpan, setShowExtraSpan] = useState(null);

  const handleClick = () => {
    navigate("/");
    setSelectedNavItem(null); // reset selected nav item when home button is clicked
  }; 

  const fetchHiddenGems = async () => {
    try {
      const getResponse = await axios.get("/api/hidden-gems");
      console.log("hidden-gems", getResponse); // Save the results in state, log for debugging
      setGemResults(getResponse.data);
      console.log("gem results", gemResults); //log for debugging
      if (
        getResponse.data &&
        typeof getResponse.data === "object" &&
        !Array.isArray(getResponse.data)
      ) {
        setGemResults(getResponse.data);  // Save the results in state
        // console.log("gem results1", gemResults); //log for debugging
        const ids = Object.values(getResponse.data).map(item => item.zone_id);
        setZoneIDs(ids);
        console.log("zoneIDs1", zoneIDs); //log for debugging
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
  fetchHiddenGems();
  }, []);

  useEffect(() => {
  console.log('gemResults2:', gemResults); //log for debugging
  // console.log('id', Object.values(gemResults)[1].zone_id)
  }, [gemResults]);

  useEffect(() => {
  console.log('zoneIDs2:', zoneIDs); // log for debugging
  // console.log('id', Object.values(gemResults)[1].zone_id)
  }, [zoneIDs]);

  // const zoneID = gemResults[0].zone_id
  const gemColour = colours.find(colour => colour.location_id == zoneIDs[0]);

  return (
    <div className="nav-container">
      <button
        className="btn menu-button"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasTop"
        aria-controls="offcanvasTop"
        onClick={handleClick}
      >
        <svg
          className="hamburger-menu"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          stroke="#ffffff"
        >
          <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
          <g
            id="SVGRepo_tracerCarrier"
            strokeLinecap="round"
            strokeLinejoin="round"
          ></g>
          <g id="SVGRepo_iconCarrier">
            {" "}
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M3 6C3 5.44772 3.44772 5 4 5H20C20.5523 5 21 5.44772 21 6C21 6.55228 20.5523 7 20 7H4C3.44772 7 3 6.55228 3 6ZM3 12C3 11.4477 3.44772 11 4 11H20C20.5523 11 21 11.4477 21 12C21 12.5523 20.5523 13 20 13H4C3.44772 13 3 12.5523 3 12ZM3 18C3 17.4477 3.44772 17 4 17H20C20.5523 17 21 17.4477 21 18C21 18.5523 20.5523 19 20 19H4C3.44772 19 3 18.5523 3 18Z"
              fill="#ffffff"
            ></path>{" "}
          </g>
        </svg>
      </button>

      <div
        className="offcanvas offcanvas-top"
        tabIndex="-1"
        id="offcanvasTop"
        aria-labelledby="offcanvasTopLabel"
      >
        <div className="offcanvas-body-top">
        <ul className="nav flex-column pe-5">
      {selectedNavItem === null || selectedNavItem === '/mostuniqueareas' ? (
        <li className="nav-item ">
          <NavLink
            to=""
            className={location.pathname === "/mostuniqueareas" ? "active-link" : ""}
            onClick={() => {
              if (selectedNavItem === '/mostuniqueareas') {
                setSelectedNavItem(null);
              } else {
                setSelectedNavItem('/mostuniqueareas');
              }
            }}
          >
            <span onClick={() => setShowExtraSpan(!showExtraSpan)}>hidden gem</span>
            <span onClick={() => setShowExtraSpan(!showExtraSpan)}>the most rarely found location this month</span>
            {selectedNavItem === '/mostuniqueareas' && (
                    <div className="result-info">

                      <div className="rank-zone-weathericon"></div>

                        <div className="rank-zone-weathericon">
                            <p className="zone">{Object.values(gemResults)[0].name}</p>
                        </div>
              <div className="tree">
                <div className="tree-left">
                  <p className="tree-title">trees</p>
                  <p className="level-of-trees">number of trees</p>
                </div>
                <div className="tree-right">
                  {/*<p className="level">level: {result.trees}</p>*/}
                  <p className="level">{Object.values(gemResults)[0].trees}</p>
                </div>
              </div>

              <div className="style">
                <div className="style-left">
                  {/*<p className="style-title">{style}</p>*/}
                  <p className="style-title">{Object.values(gemResults)[0].main_style}</p>
                  <p className="architecture">architecture</p>
                </div>
                <div className="style-right">
                  <p className="building-counting">
                    {/*{result.style}{result.style === 1 ? " building" : " buildings"}*/}
                    {Object.values(gemResults)[0].main_style_amount}
                  </p>
                </div>
              </div>
              <div className="color-pallete">
                <div className="color-pallete-left">
                  <p className="colors-title">colors</p>
                </div>

                {/*  below works*/}
                <div className="color-pallete-right">
                  {gemColour && gemColour.colors.map((hex, index) => (
                    <div
                        key={index}
                        className="hexdiv"
                        style={{ backgroundColor: hex }}
                        ></div>
                    ))}
                </div>

              </div>

              </div>)}
          </NavLink>
        </li>
      ) : null}
      {selectedNavItem === null || selectedNavItem === '/contact' ? (
        <li className="nav-item ">
          <NavLink
            to="/contact"
            className={location.pathname === "/contact" ? "active-link" : ""}
            onClick={() => {
              if (selectedNavItem === '/contact') {
                setSelectedNavItem(null);
              } else {
                setSelectedNavItem('/contact');
              }
            }}
          >
            <span>contact</span>
            <span>feedback and questions</span>
          </NavLink>
        </li>
      ) : null}
      {selectedNavItem === null || selectedNavItem === '/about' ? (
        <li className="nav-item ">
          <NavLink
            to="/about"
            className={location.pathname === "/about" ? "active-link" : ""}
            onClick={() => {
              if (selectedNavItem === '/about') {
                setSelectedNavItem(null);
              } else {
                setSelectedNavItem('/about');
              }
            }}
          >
            <span>about this web app</span>
            <span>user help information</span>
          </NavLink>
        </li>
      ) : null}
    </ul>
    {selectedNavItem === null ? null : (
            <Routes>
              <Route path="/mostuniqueareas" element={<MostUniqueAreas />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/about" element={<AboutThisWeb />} />
            </Routes>
          )}
        </div>
      </div>
    </div>
  );
}