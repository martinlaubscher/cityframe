// SearchResult.jsx
import axios from "axios";

export default function SearchResult({ results }) {
  return (
    <div>
      {results.map((result) => (
        <div key={result.id}>
          <h2>Place ID: {result.id}</h2>
          <p>Busyness: {result.busyness}</p>
          <p>Trees: {result.trees}</p>
          <p>Style: {result.style}</p>
        </div>
      ))}
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
      searchOptions.tree ? 1 : 0,
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
      
      time: searchOptions.datetime,
      busyness: searchOptions.busyness,
      trees: searchOptions.tree ? 1 : 0,
      style: searchOptions.style,
    });

    if (response.data && typeof response.data === 'object' && !Array.isArray(response.data)) {
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
