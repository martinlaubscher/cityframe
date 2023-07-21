import React from 'react';
import Card from 'react-bootstrap/Card';

const SearchResult = ({ results }) => (
  <div>
    {results.map((result, index) => (
      <Card style={{ width: '18rem' }} key={index}>
        <Card.Body>
          <Card.Title>{result.name}</Card.Title>
          <Card.Text>
            Score: {result.score}<br/>
            Busyness: {result.busyness}<br/>
            Trees: {result.trees ? "Yes" : "No"}<br/>
            Style: {result.style}
          </Card.Text>
        </Card.Body>
      </Card>
    ))}
  </div>
);

export default SearchResult;
