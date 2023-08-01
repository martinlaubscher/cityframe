import "./MapBackground.css";
import React from "react";
import axios from "@/axiosConfig";
import { MapContainer, TileLayer, Marker, Popup, Polygon } from "react-leaflet";
//import geodata from '../dummydata/geodata'

export default function Map(props) {
  const defaultOptions = { color: "#808080", weight: 1, fillOpacity: 0 };
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

  React.useEffect(() => {
    let busynessZonesObj = {};
    for (let level in props.busynessZones) {
      props.busynessZones[level].forEach((zone) => {
        busynessZonesObj[zone] = level;
      });
    }
    setBusynessZonesObj(busynessZonesObj);
  }, [props.busynessZones]);

  const [busynessZonesObj, setBusynessZonesObj] = React.useState(null);

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
      polygons = geojsonData.features.map((feature, idx) => {
        var path;

        const busynessLevel =
          busynessZonesObj && busynessZonesObj[feature.properties.location_id];
        if (busynessLevel) {
          path = {
            fillColor: getBusynessColor(busynessLevel),
            color:"black",
            weight:0.3,
            // stroke: true
            fillOpacity: 0.9
          };
          // console.log("Path set with busyness color:", path);
        } else {
          path = { color: "white", weight: 0.5, fillOpacity: 0.3};
          // console.log("Path set with default options:", path);
        }

        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
          return (
            <Polygon
              key={`${idx}-${polygonIndex}`}
              positions={polygon[0].map((coord) => [coord[1], coord[0]])}
              pathOptions={path}
            >
              {console.log("Polygon properties:", feature.properties, path)}
            </Polygon>
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
