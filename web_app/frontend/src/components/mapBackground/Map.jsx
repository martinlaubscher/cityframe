// import {MapContainer, TileLayer, Marker, Popup, Polygon} from 'react-leaflet'
import "./MapBackground.css";
import React from "react";
import axios from "@/axiosConfig";
import { MapContainer, TileLayer, Marker, Popup, Polygon } from "react-leaflet";
//import geodata from '../dummydata/geodata'

export default function Map(props) {
  const defaultOptions = { color: "#808080", weight: 1, fillOpacity: 0 };
  //   const purpleOptions = {
  //     color: "purple",
  //     weight: 2,
  //     fillColor: "green",
  //     fillOpacity: 0.5,
  //   };
  const homepageDefaultOptions = {color: "white", weight: 1, fillOpacity: 0.5 }
  const [geojsonData, setGeojsonData] = React.useState(null);

  function handleClick() {
    console.log("She doesn't even go here");
  }

  React.useEffect(() => {
    axios
      .get("/assets/manhattan_taxi_zones.geojson")
      .then((response) => {
        setGeojsonData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching geojson data: ", error);
      });
  }, []);

  console.log("Geojson data?", geojsonData);

  console.log("busynessZones-Map recieve the prop:", props.busynessZones);

  function handleClick() {
    console.log("She doesn't even go here");
  }

  function getColour(rank) {
    // Define the hue and lightness range for the heatmap. Saturation remains at 100%
    const colourVar = (11 - rank) * 10;
    const hue = colourVar + 230; // PURPLE!!!

    const lightness = 90 - colourVar / 2;
    return `hsl(${hue}, ${100}%, ${lightness}%)`;
  }

  // ======================homepage heatmap============================
  console.log("busynessZones-Map recieve the prop:", props.busynessZones);

  const getBusynessColor = (busynessLevel) => {
    const busynessColors = {
      1: "#FFE16D",
      2: "#FFCC69",
      3: "#FFAE6D",
      4: "#FF937A",
      5: "#FF7D8B",
    };
    return busynessColors[busynessLevel];
  };
  

  
  // ================================================================================

  var polygons;
  if (geojsonData) {
    if (props.isSearched) {
      polygons = geojsonData.features.map((feature, idx) => {
        var path;
        var click;

        var placeRank = props.searchResults.find(
          (place) => place.id === feature.properties.location_id
        );

        if (placeRank) {
          path = {
            color: "purple",
            weight: 2,
            fillColor: getColour(placeRank.rank),
            fillOpacity: 0.8,
          };
          click = () => props.buildlist(feature, placeRank);
        } else {
          path = defaultOptions;
          click = handleClick;
        }

        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
          return (
            <Polygon
              key={`${idx}-${polygonIndex}`}
              positions={polygon[0].map((coord) => [coord[1], coord[0]])} // swap lat and lng
              pathOptions={path}
              eventHandlers={{
                click: click,
              }}
            />
          );
        });
      });
    }
    // ======================homepage heatmap============================
    else {
      // polygons = geojsonData.features.map((feature, idx) => {
      //   return feature.geometry.coordinates.map((polygon, polygonIndex) => {
      //     return (
      //       <Polygon
      //         key={`${idx}-${polygonIndex}`}
      //         positions={polygon[0].map((coord) => [coord[1], coord[0]])} // swap lat and lng
      //         pathOptions={getStyle(feature)}
      //       />
      //     );
      //   });
      // });
      polygons = geojsonData.features.map((feature, idx) => {
        var path;
        // var click;
      
        // form props.busynessZones get feature's busyness level
        const busynessLevel = props.busynessZones && Object.keys(props.busynessZones).find(
          (level) => {
            const includesLocation = props.busynessZones[level].includes(feature.properties.location_id);
            console.log("iterating feature:",feature.properties.location_id);
            console.log(`Checking level ${level}: ${includesLocation ? 'matches' : 'does not match'}`);
            console.log(includesLocation); 
            return includesLocation;
          }
        );
        if (busynessLevel) {
          path = {
            // color: getBusynessColor(busynessLevel),
            color: "red",
            weight: 2,
            fillOpacity: 0.8,
          };
          console.log("Path set with busyness color:", path.color);
        } else {
          path = homepageDefaultOptions;
          console.log("Path set with default options:", path);
        }
        
      
        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
          return (
            <Polygon
              key={`${idx}-${polygonIndex}`}
              positions={polygon[0].map((coord) => [coord[1], coord[0]])} 
              pathOptions={path}
            />
          );
        });
      });
      
    }
  }

  return (
    <div className="Map--div">
      <MapContainer
        center={[40.7831, -73.9712]}
        zoom={13}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {polygons}
      </MapContainer>
    </div>
  );
}
