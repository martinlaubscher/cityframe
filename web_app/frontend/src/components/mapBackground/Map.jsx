import {MapContainer, TileLayer, ZoomControl, Marker, Popup, Polygon} from 'react-leaflet'
import "./MapBackground.css"
import React from 'react'
import axios from '@/axiosConfig';

//import geojsonData from '../dummydata/geodata'

export default function Map(props) {

    const defaultOptions = {color: '#808080', weight: 1, fillColor:"blue", fillOpacity: 0}
    //const purpleOptions = {color: "purple", weight: 2, fillColor:"green", fillOpacity: 0.5}
    
    const [geojsonData, setGeojsonData] = React.useState(null);

    React.useEffect(() => {
        axios.get('/assets/manhattan_taxi_zones.geojson')
            .then(response => {
                setGeojsonData(response.data);
            })
            .catch(error => {
                console.error("Error fetching geojson data: ", error);
            });
    }, []);
    


    function handleClick(){
        console.log("She doesn't even go here")
    }

    function rankColour(rank) {

        // Define the hue and lightness range for the heatmap. Saturation remains at 100%
        const colourVar = (10 - rank)
        //const hue = colourVar + 230; // PURPLE!!!
        const hue = 110+rank*10
        console.log(rank, hue)

        const lightness = 90 - (colourVar * 5);
        return `hsl(${hue}, ${100}%, ${50}%)`

    }

    function rankOutline(rank){
        if (rank === 1){
            return "#E6BE00"
        }
        else if (rank === 2){
            return "#D7D7D7"
        }
        else if (rank === 3){
            return "#A55028"
        }
        else{
            return "#9B9169"
        }
    }
    
    function busyColour(busy){
        const hue = busy*55
        return `hsl(${hue}, ${100}%, ${50}%)`

    }

    var polygons
    if (geojsonData){
        var path
        var click
        if (props.isSearched){

        polygons=geojsonData.features.map((feature, idx) => {

        
        var placeRank = props.searchResults.find(place => place.id === feature.properties.location_id)

        if (placeRank){
            path= {color: "purple", weight: 2, fillColor:rankColour(placeRank.rank), fillOpacity: 1}
            click= () => props.buildlist(feature, placeRank)
        }
        else{
            path=defaultOptions
            click= handleClick
        }

        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
            return(
            <Polygon
                key={`${idx}-${polygonIndex}`}
                positions={polygon[0].map(coord => [coord[1], coord[0]])} // swap lat and lng
                pathOptions={path}
                eventHandlers={{
                    click: click
                }}
            />)
            });
    })}

    else{
        //path={color: '#808080', weight: 1, fillColor:"blue", fillOpacity: 0.5}

        polygons=geojsonData.features.map((feature, idx) => {
            console.log(feature)
            path={color: '#808080', weight: 1, fillColor: busyColour(1), fillOpacity: 0.5}
            return feature.geometry.coordinates.map((polygon, polygonIndex) => {
                return(
                <Polygon
                    key={`${idx}-${polygonIndex}`}
                    positions={polygon[0].map(coord => [coord[1], coord[0]])} // swap lat and lng
                    pathOptions={path}
                    eventHandlers={{
                        click: handleClick
                    }}
                />)
                });
            })

        }
    }

    return (
        <div className="Map--div">
            <MapContainer center={[40.7831, -73.9712]} zoom={13} scrollWheelZoom={true} zoomControl={false}>
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                 {
                    //<ZoomControl position={'topright'} />
                }
                {polygons}
            </MapContainer>
        </div>)
}