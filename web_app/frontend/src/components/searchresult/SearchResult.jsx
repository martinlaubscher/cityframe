// SearchResult.jsx
import axios from "axios";

export default function SearchResult({ results }) {
  return (
    <div>
      {results.map((result, index) => (
        <div key={index}>
          {/* render search result */}
          <p>{result.name}</p>
          <p>{result.datetime}</p>
          {/* ... other result data */}
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

    const response = await axios.post("/api/submit-main", {
      time: searchOptions.datetime,
      busyness: searchOptions.busyness,
      trees: searchOptions.tree ? 1 : 0,
      style: searchOptions.style,
    });

    return response.data;
  } catch (error) {
    console.error("Error:", error);
    return []; // Return an empty array in case of error or no data
  }
}
