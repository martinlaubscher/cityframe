// SearchResult.jsx
import axios from 'axios';

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
    const response = await axios.get('/api/submit-main', {
      params: {
        time: searchOptions.datetime,
        busyness: searchOptions.busyness,
        trees: searchOptions.tree ? 1 : 0,
        style: searchOptions.style
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    return []; // Return an empty array in case of error or no data
  }
}
