// SearchResult.jsx
import axios from '@/axiosConfig';
import "./SearchResultCSS.css"

export default function SearchResult({ results }) {
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
            <img
              src={`https://picsum.photos/1020/1080?random=${result.id}`}
              className="d-block w-100 image-border"
              alt={`Place ${result.id}`}
            />
            <div className="carousel-caption caption-background">
              <h2>Zone ID: {result.id}</h2>
              <p>Busyness: {result.busyness}</p>
              <p>Trees: {result.trees}</p>
              <p>Style: {result.style}</p>
              <p>{result.dayTimeDescription}</p> {/* Add this line to show the description of the day time */}
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
    // Get the golden hour and sunset times
    // const goldenHourResponse = await axios.get(`/api/golden-hour/${searchOptions.datetime.toISOString().split('T')[0]}`);
    const currentSuntimesResponse = await axios.get(`/api/current-suntimes/datetime`);
    const goldenHour = goldenHourResponse.data;
    const currentSuntimes = currentSuntimesResponse.data;

    const response = await axios.post("http://127.0.0.1:8000/api/submit-main", {
      time: searchOptions.datetime,
      busyness: searchOptions.busyness,
      trees: searchOptions.tree ? 1 : 0,
      style: searchOptions.style,
    });

    if (
      response.data &&
      typeof response.data === "object" &&
      !Array.isArray(response.data)
    ) {
      const results = Object.entries(response.data).map(([key, value]) => {
        // Calculate the description of the day time
        let dayTimeDescription = "";
        if (/* Check if the chosen time is in golden hour */ false) {
          dayTimeDescription = "Golden Hour";
        } else if (/* Check if the chosen time is in blue hour */ false) {
          dayTimeDescription = "Blue Hour";
        } else if (/* Check if the chosen time is in sunrise */ false) {
          dayTimeDescription = "Sunrise";
        } else if (/* Check if the chosen time is in sunset */ false) {
          dayTimeDescription = "Sunset";
        }

        return {
          id: key,
          dayTimeDescription,
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
