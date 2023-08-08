import {
  MapContainer,
  TileLayer,
  Polygon,
  Popup
} from "react-leaflet";
import "./MapBackground.css";
import React from "react";
import axios from "@/axiosConfig";

export default function Map({viewMode, zones, ...props}) {
  const defaultOptions = {
    color: "#808080",
    weight: 1,
    fillColor: "blue",
    fillOpacity: 0,
  };


  const [geojsonData, setGeojsonData] = React.useState(null);
  const [zoneData, setZoneData] = React.useState(null);
  const mapRef = React.useRef(null);


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

  React.useEffect(() => {
    axios
      .get("/api/zonedata/")
      .then((response) => {
        setZoneData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching zone data: ", error);
      });
  }, []);


  function setCenter(feature){ //set the map to focus on the clicked polygon
    const center = L.latLngBounds(feature.geometry.coordinates).getCenter(); //get center of polygon

    if (mapRef.current) {
      const map = mapRef.current;
      const height = map.getSize().y;
      const zoom = map.getZoom();
      const lat = center.lng - (height / (2 ** zoom)) * 0.32; //make the actual centre slightly below the coordinates 
      mapRef.current.setView([lat, center.lat]); //no idea whose idea it was to swap lat and lng for setting the view but this sets the view correctly
    }
  }

  function handleClick(feature) {
    //console.log("She doesn't even go here");
    setCenter(feature)
  }

  function listBuild(feature, rank){
    props.buildlist(feature, rank)
    setCenter(feature)
  }

  function rankColour(rank) {
    // Define the hue and lightness range for the heatmap. Saturation remains at 100%
    const colourVar = 10 - rank;
    //const hue = colourVar + 230; // PURPLE!!!
    // console.log(rank, hue);
    const lightness = 54.2 + rank * 4.2;
    return `hsl(${230}, ${100}%, ${lightness}%)`;
  }


  // ======================homepage heatmap============================
  // console.log("busynessZones-Map recieve the prop:", props.busynessZones);

  const getBusynessColor = (busynessLevel) => {
    const busynessColors = {
      1: "#99EE47",
      2: "#DCD029",
      3: "#FFD944",
      4: "#F9A75E",
      5: "#FF7D8B",
    };
    return busynessColors[busynessLevel];
  };

  const [busynessZonesObj, setBusynessZonesObj] = React.useState(null);
  // const [prevBusynessLevel, setPrevBusynessLevel] = useState(null);

  React.useEffect(() => {
    let busynessZonesObj = {};
    for (let level in props.busynessZones) {
      if (props.busynessZones[level]) {
        props.busynessZones[level].forEach((zone) => {
          busynessZonesObj[zone] = level;
        });
      }
    }
    setBusynessZonesObj(busynessZonesObj);
  }, [props.busynessZones]);

  function capitaliseFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  // useEffect(() => {
  //   setPrevBusynessLevel(busynessZonesObj);
  // }, [busynessZonesObj]);

  // ================================================================================

  var polygons;
  if (geojsonData && zoneData) {
    var path;
    var click;

    // if (props.isSearched && busynessZonesObj === prevBusynessLevel) {

    if (viewMode === 'results') {
      // console.log("map:result")
      polygons = geojsonData.features.map((feature, idx) => {
        var placeRank = props.searchResults.find(
          (place) => place.id === feature.properties.location_id
        );

        if (placeRank) {
          path = {
            color: "purple",
            weight: 2,
            fillColor: rankColour(placeRank.rank),
            fillOpacity: 1,
          };
          click = () => listBuild(feature, placeRank);
        } else {
          path = defaultOptions;
          click = () => handleClick(feature);
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
      // if(props.busynessZones){
      console.log(zoneData)
      polygons = geojsonData.features.map((feature, idx) => {
        var path;

        let busynessLevel

        if (busynessZonesObj) {
          busynessLevel = busynessZonesObj[feature.properties.location_id];
        }
        if (busynessLevel) {
          path = {
            fillColor: getBusynessColor(busynessLevel),
            color: "black",
            weight: 1,
            fillOpacity: 0.9,
            dashArray: "5, 5",
          };
        } else {
          path = {
            color: "black",
            weight: 1,
            fillOpacity: 0,
            dashArray: "5, 5", // add dash line style
          };
        }

        const locationId = feature.properties.location_id;
        const zoneDetails = zoneData[locationId];

        // Make sure zoneDetails exists before accessing properties
        const zoneName = zoneDetails ? zoneDetails.zone : "Unknown Zone";
        const architectureStyle = zoneDetails ? zoneDetails.main_style : "Unknown Style";
        const treeCount = zoneDetails ? zoneDetails.trees : "Unknown";
        const zoneType = zoneDetails ? zoneDetails.zone_type : "Unknown Type";

        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
          return (
            <Polygon
              key={`${idx}-${polygonIndex}`}
              positions={polygon[0].map((coord) => [coord[1], coord[0]])}
              pathOptions={path}
              eventHandlers={{
                click: click,
              }}
            >
              <Popup>
                <div>
                  <p className="popup-title">{zoneName}</p>
                  <p className="popup-level">level {zones[locationId]}/5</p>
                  <div className="popup-details">
                    <p>architecture style:</p>
                    <p className="popup-details-value">{architectureStyle}</p>
                  </div>
                  <div className="popup-details">
                    <p>zone type:</p>
                    <p className="popup-details-value">{zoneType}</p>
                  </div>
                  <div className="popup-details">
                    <p>trees:</p>
                    <p className="popup-details-value">{treeCount}</p>
                  </div>
                </div>
              </Popup>
              {/*{console.log("Polygon properties:", feature.properties, path)}*/}
            </Polygon>
          );
        });
      });
    }
  }
    

  return (
    <div className="Map--div">
      <MapContainer
        ref={mapRef}
        center={[40.7831, -73.9712]}
        zoom={12}
        scrollWheelZoom={true}
        maxZoom={14}
        minZoom={11}
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
