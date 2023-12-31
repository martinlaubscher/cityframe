import React, {useState, useEffect, useRef} from "react";
import axios from "@/axiosConfig";
import "./SearchResultCSS.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {getIcon} from "../weatherInfo/WeatherHelpers";
import goldenIcon from "../../assets/goldenhour.png";
import goldenIcon_avif from "../../assets/goldenhour.avif";
import {getImageUrlSmallById} from "./ResultPictures";

let style;

export default function SearchResult({results, searchOptions}) {
  const [goldenHourStatus, setGoldenHourStatus] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const carouselRef = useRef(null);
  const errorRef = useRef(null);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    Promise.all(
      results.map((result) => getGoldenOrBlueHour(result.dt_iso))
    ).then((statuses) => setGoldenHourStatus(statuses));
  }, [results]);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (isMounted) {
      if (results.length === 0) {
        errorRef.current?.scrollIntoView({behavior: 'smooth'});
      } else {
        setActiveIndex(0);
        carouselRef.current?.scrollIntoView({behavior: 'smooth'});
      }
    }
  }, [results, isMounted]);

  useEffect(() => {
    if (!isMounted || !carouselRef.current) return;
    const updateActiveIndex = (event) => {
      const newIndex = Array.from(carouselRef.current.children[1].children).indexOf(event.relatedTarget);
      setActiveIndex(newIndex);
    };
    carouselRef.current.addEventListener('slid.bs.carousel', updateActiveIndex);

    return () => {
      carouselRef.current.removeEventListener('slid.bs.carousel', updateActiveIndex);
    };
  }, [isMounted]);

  if (results.length === 0) {
    return (
      <div className="error-inner" ref={errorRef}>
        <span className="error-alert">Nothing here!</span>
        <span className="error-alert">More photo spots await! 📷</span>
      </div>
    );
  }

  return (
    <div id="carouselExampleIndicators" className="carousel slide" ref={carouselRef}>
      <div className="carousel-indicators">
        {results.map((result, index) => (
          <button
            key={result.id}
            type="button"
            data-bs-target="#carouselExampleIndicators"
            data-bs-slide-to={index}
            className={index === activeIndex ? "active" : ""}
            aria-current={index === activeIndex ? "true" : "false"}
            aria-label={`Slide ${index + 1}`}
          />
        ))}
      </div>
      <div className="carousel-inner">
        {results.map((result, index) => (
          <div
            key={result.id}
            className={`carousel-item ${index === activeIndex ? "active" : ""}`}
          >
            <div className="result-info">
              <div className="rank-zone-weathericon">
                <div className="rank-zone">
                  <p className="rank">{result.rank}</p>
                  <p className="zone">{result.zone}</p>
                </div>
                <div className="weathericon">
                  <FontAwesomeIcon
                    icon={getIcon(result.weather.weather_icon)}
                    size="2x"
                  />
                </div>
              </div>
              <div className="datetime result-param">
                <div className="datetime-left">
                  <p className="datetime-title">date/time</p>
                </div>
                {goldenHourStatus[index] ? (
                    <div className="datetime-right-time-golden-blue-hour">
                      <div className="datetime-icon-container">
                        <picture>
                          <source
                              className="logo-image"
                              srcSet={goldenIcon_avif}
                              type="image/avif"
                              style={{height: "25px"}}
                          />
                          <img
                              src={goldenIcon}
                              alt="golden icon"
                              style={{height: "25px", width: "auto"}}
                          />
                        </picture>
                      </div>
                      <div className="datetime-text-container">
                        <p className="result-date-time">{result.dt_iso}</p>
                        <p className="golden-blue-hour">
                          this is golden/blue hour
                        </p>
                      </div>
                    </div>
                ) : (
                    <div className="datetime-right-only-time">
                      <p>{result.dt_iso}</p>
                    </div>
                )}
              </div>
              <div className="busyness result-param">
                <div className="busyness-left">
                  <p className="busyness-title">busyness</p>
                  <p className="level-of-busyness">level of busyness</p>
                </div>
                <div className="busyness-right">
                  <p className="level">level: {result.busyness}</p>
                </div>
              </div>
              <div className="tree result-param">
                <div className="tree-left">
                  <p className="tree-title">trees</p>
                  <p className="level-of-trees">more or less trees</p>
                </div>
                <div className="tree-right">
                  <p className="level">level: {result.trees}</p>
                </div>
              </div>
              <div className="style result-param">
                <div className="style-left">
                  <p className="style-title">{result.architecture}</p>
                  <p className="architecture">architecture style</p>
                </div>
                <div className="style-right">
                  <p className="building-counting">
                    {result.style}
                    {result.style === 1 ? " building" : " buildings"}
                  </p>
                </div>
              </div>
              <div className="type result-param">
                <div className="type-left">
                  <p className="type-title">type</p>
                  <p className="type-desc">zone type</p>
                </div>
                <div className="type-right">
                  <p className="type-percent">{result.zone_type}</p>
                </div>
              </div>
              <div className="color-pallete result-param">
                <div className="color-pallete-left">
                  <p className="colors-title">colors</p>
                  <p className="colors-desc">common colors in this zone</p>
                </div>
                <div className="color-pallete-right search-pallete">
                  {result.pallete.map((hex, index) => (
                    <div
                      key={index}
                      className="hexdiv"
                      style={{backgroundColor: hex}}
                    ></div>
                  ))}
                </div>
              </div>

              <div className="pictures">
                <img
                  src={getImageUrlSmallById(result.id)}
                  alt={`Image ${index}`}
                />
                {/*{console.log(*/}
                {/*  "result.id:",*/}
                {/*  result.id,*/}
                {/*  "url:",*/}
                {/*  getImageUrlSmallById(result.id)*/}
                {/*)}*/}
              </div>
            </div>
          </div>
        ))}
      </div>
      <button
        className="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExampleIndicators"
        data-bs-slide="prev"
      >
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Previous</span>
      </button>
      <button
        className="carousel-control-next"
        type="button"
        data-bs-target="#carouselExampleIndicators"
        data-bs-slide="next"
      >
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Next</span>
      </button>
    </div>
  );
}

async function fetchCsrfToken() {
  const response = await axios.get('/api/get-csrf-token/');
  return response.data.csrfToken;
}

export async function handleSearch(searchOptions) {
  try {
    // Log the response data to the console
    // console.log(
    //   "searchOptions:",
    //   "time:",
    //   searchOptions.datetime,
    //   "busyness:",
    //   searchOptions.busyness,
    //   "trees:",
    //   // searchOptions.tree ? 1 : 0,
    //   searchOptions.tree,
    //   "style:",
    //   searchOptions.style,
    //   "weather:",
    //   searchOptions.weather
    // );

    // save style at request time to use for results later
    style = searchOptions.style;

    // add weather filter
    let data = {
      busyness: searchOptions.busyness,
      trees: searchOptions.tree,
      time: searchOptions.datetime,
      style: searchOptions.style,
      zone_type: searchOptions.zone_type,

      ...(searchOptions.weather !== "All"
        ? {weather: searchOptions.weather}
        : {}),
    };

    const csrfToken = await fetchCsrfToken();

    const response = await axios.post("/api/submit-main", data, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    });
    // console.log("submit-main", response);
    if (
      response.data &&
      typeof response.data === "object" &&
      !Array.isArray(response.data)
    ) {
      return Object.values(response.data).sort((a, b) => a.rank - b.rank);
    }

    return [];
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
}

export async function getGoldenOrBlueHour(dateTime_dt_iso) {
  let dateTime_dt_iso_split = dateTime_dt_iso.split(" ");
  let date_dt_iso = dateTime_dt_iso_split[0];
  // console.log("Date: " + date_dt_iso);

  let timeOfSun__dt_iso = await axios.get(`/api/suntimes/${date_dt_iso}/`);
  // console.log("timeOfSun: " + JSON.stringify(timeOfSun__dt_iso.data));

  const dateTimeDate = new Date(dateTime_dt_iso);
  const goldenHourMorningDate = new Date(
    timeOfSun__dt_iso.data.golden_hour_morning
  );
  const goldenHourEveningDate = new Date(
    timeOfSun__dt_iso.data.golden_hour_evening
  );
  const blueHourMorningDate = new Date(
    timeOfSun__dt_iso.data.blue_hour_morning
  );
  const blueHourEveningDate = new Date(
    timeOfSun__dt_iso.data.blue_hour_evening
  );

  if (
    (blueHourMorningDate <= dateTimeDate &&
      dateTimeDate <= goldenHourMorningDate) ||
    (goldenHourEveningDate <= dateTimeDate &&
      dateTimeDate <= blueHourEveningDate)
  ) {
    // console.log("The time is within the golden hour.");
    return true;
  } else {
    // console.log("The time is not within the golden hour.");
    return false;
  }
}
