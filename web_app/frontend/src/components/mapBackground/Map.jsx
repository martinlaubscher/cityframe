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
  const [geojsonData, setGeojsonData] = React.useState(null);

  // 定义繁忙程度对应的颜色
  const busynessColors = {
    1: "#FFE16D",
    2: "#FFCC69",
    3: "#FFAE6D",
    4: "#FF937A",
    5: "#FF7D8B",
  };

  // 获得繁忙程度数据
  async function getAllBusyness() {
    try {
      const response = await axios.get(`/api/current-busyness`);
      console.log(response.data);
      return response.data;
    } catch (error) {
      console.error("There was an error retrieving the data: ", error);
    }
  }

  // 根据繁忙程度获得样式
  function getStyle(feature) {
    const busynessLevel = feature.properties.busynessLevel;
    return {
      fillColor: busynessColors[busynessLevel],
      weight: 2,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: 0,
    };
  }

  // 从后端获得GeoJSON数据并加载到地图上
  React.useEffect(() => {
    axios
      .get("/assets/manhattan_taxi_zones.geojson")
      .then((response) => {
        const geojsonData = response.data;
        // 将繁忙程度数据添加到GeoJSON数据中
        getAllBusyness().then((busynessData) => {
          for (const feature of geojsonData.features) {
            const zoneId = feature.properties.zoneId;
            if (zoneId in busynessData) {
              feature.properties.busynessLevel = busynessData[zoneId];
            } else {
              feature.properties.busynessLevel = 1;
            }
          }
          setGeojsonData(geojsonData);
        });
      })
      .catch((error) => {
        console.error("There was an error retrieving the data: ", error);
      });
  }, []);

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
    } else {
      polygons = geojsonData.features.map((feature, idx) => {
        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
          return (
            <Polygon
              key={`${idx}-${polygonIndex}`}
              positions={polygon[0].map((coord) => [coord[1], coord[0]])} // swap lat and lng
              pathOptions={getStyle(feature)}
              eventHandlers={{
                click: handleClick,
              }}
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
