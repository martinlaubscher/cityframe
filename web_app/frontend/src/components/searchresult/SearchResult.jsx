// SearchResult.jsx
import axios from "axios";
import "./SearchResultCSS.css"

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
            style={{
              // backgroundImage: `url(https://picsum.photos/1920/1080?random=${result.id})`,
            }}
          >
            <div className="overlay-info">
              <div className="info-zone-style-buyness-tree">
                <div className="info-zone-style">
                  <p>{result.zone}</p>
                  <p>{result.style}  {searchOptions.style}  buildings</p>
                </div>
                <div className="info-busyness-tree">
                  <p>BUSYNESS {result.busyness}</p>
                  <p>TREES {result.trees}</p>
                </div>
              </div> 
              <div className="info-time">
                <p>{result.dt_iso}</p>
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
      const results = Object.entries(response.data).map(([key, value]) => {
        return {
          id: key,
          ...value,
        };
      });
      return results;
    }

    return [];
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
}
