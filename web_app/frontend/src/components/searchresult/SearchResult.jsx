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
              <div className="result-rank-zonename">
                <div className="result-rank">
                  <p>{result.rank}.</p>
                </div>
                <div className="result-zonename">
                  <p>{result.zone}</p>
                </div>

                <div className="result-busyness">
                  <p>BUSYNESS {result.busyness}</p>
                </div>
                <div className="result-trees">
                  <p>TREES {result.trees}</p>
                </div>
                <div className="result-architecture">
                  <p>
                    {result.style} {style} buildings
                  </p>
                </div>
                <div className="result-colors"></div>
                <div className="result-date-time">
                  {" "}
                  <p>{result.dt_iso}</p>
                </div>
                <div className="result-pictures">
                  <img
                    src={`https://picsum.photos/1920/1080?random=${result.id}`}
                    alt={`Image ${index}`}
                  />
                </div>
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
