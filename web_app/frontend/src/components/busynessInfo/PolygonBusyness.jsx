import React from 'react';
import { Polygon } from 'react-leaflet';

function getColor(busyness) {
  const colorMap = {
    1: '#FFE16D',
    2: '#FFCC69',
    3: '#FFAE6D',
    4: '#FF937A',
    5: '#FF7D8B'
  };
  return colorMap[busyness];
}

function PolygonBusyness({ feature, busyness }) {

  const locationId = feature.properties.location_id;

  return (
    <Polygon
      key={locationId}
      positions={feature.geometry.coordinates[0].map(([lng, lat]) => [lat, lng])}
      color={getColor(busyness)}
    />
  );
}

export default PolygonBusyness;
