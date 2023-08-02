// SearchResult.jsx
import axios from "@/axiosConfig";
import "./SearchResultCSS.css";

let style;

export default function SearchResult({ results, searchOptions }) {
  return (
    <div id="carouselExampleIndicators" className="carousel slide">
      <div className="carousel-indicators">
        {results.map((result, index) => (
          <button
            key={result.id}
            type="button"
            data-bs-target="#carouselExampleIndicators"
            data-bs-slide-to={index}
            className={index === 0 ? "active" : ""}
            aria-current={index === 0 ? "true" : "false"}
            aria-label={`Slide ${index + 1}`}
          />
        ))}
      </div>
      <div className="carousel-inner">
        {results.map((result, index) => (
          <div
            key={result.id}
            className={`carousel-item ${index === 0 ? "active" : ""}`}
          >
            <div className="result-info">
              <div className="rank-zone">
                <p className="rank">{result.rank}</p>
                <p className="zone">{result.zone}</p>
              </div>
              <div className="busyness">
                <div className="busyness-left">
                  <p className="busyness-title">busyness</p>
                  <p className="level-of-busyness">level of busyness</p>
                </div>
                <div className="busyness-right">
                  <p className="level">level: {result.busyness}</p>
                </div>
              </div>
              <div className="tree">
                <div className="tree-left">
                  <p className="tree-title">trees</p>
                  <p className="level-of-trees">level of trees</p>
                </div>
                <div className="tree-right">
                  <p className="level">level: {result.trees}</p>
                </div>
              </div>

              <div className="style">
                <div className="style-left">
                  <p className="style-title">{style}</p>
                  <p className="architecture">architecture</p>
                </div>
                <div className="style-right">
                  <p className="building-counting">
                    building counting {result.style}
                  </p>
                </div>
              </div>
              <div className="color-pallete">
                <div className="color-pallete-left">
                  <p className="colors-title">colors</p>
                </div>
                <div className="color-pallete-right">
                  {result.pallete.map((hex) => (
                    <div
                      className="hexdiv"
                      style={{ backgroundColor: hex }}
                    ></div>
                  ))}
                </div>
              </div>
              <div className="datetime">
                <div className="datetime-left">
                  <p className="datetime-title">date/time</p>
                </div>
                <div className="datetime-right">
                  <p >{result.dt_iso}</p>
                </div>
              </div>
              <div className="pictures">
                <img
                  src={`https://picsum.photos/1920/1080?random=${result.id}`}
                  alt={`Image ${index}`}
                />
                {/* <img src={result.imageUrl} alt={`Image ${index}`} /> */}
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

export async function handleSearch(searchOptions) {
  try {
    // Log the response data to the console
    console.log(
      "time:",
      searchOptions.datetime,
      "busyness:",
      searchOptions.busyness,
      "trees:",
      // searchOptions.tree ? 1 : 0,
      searchOptions.tree,
      "style:",
      searchOptions.style
    );

    // Frontend: Implemented CORS in the local environment to facilitate real-time visualization
    // of changes made to the frontend code. This allows the frontend to instantly view the modifications
    // on the web page while utilizing data obtained from the backend, eliminating the need to run "npm build"
    // and handle static files every time.

    // save style at request time to use for results later
    style = searchOptions.style;

    // Notice：de-comment in final version
    const response = await axios.post("/api/submit-main", {
      //Notice：comment before commit
      // const response = await axios.post("http://127.0.0.1:8000/api/submit-main", {

      busyness: searchOptions.busyness,
      trees: searchOptions.tree,
      time: searchOptions.datetime,
      style: searchOptions.style,
    });

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
