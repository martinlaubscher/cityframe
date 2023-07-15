import  { useEffect, useRef } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';

const MapBackground = () => {
  const mapRef = useRef(null);

  useEffect(() => {
    const mapElement = mapRef.current;

    if (!mapElement) return;

    const map = new Map({
      target: mapElement,
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      view: new View({
        center: [0, 0],
        zoom: 2,
      }),
    });

    return () => {
      map.setTarget(null);
    };
  }, []);

  return <div ref={mapRef} className="map-background" />;
};

export default MapBackground;