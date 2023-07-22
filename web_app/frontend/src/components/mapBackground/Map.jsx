import {MapContainer, TileLayer, Marker, Popup, Polygon} from 'react-leaflet'
import "./MapBackground.css"
import React from 'react'

import geodata from '../dummydata/geodata'
import { polygon } from 'leaflet'

export default function Map(props) {
    const [marker, setMarker] = React.useState([40.7831, -73.9712])
    const defaultOptions = {color: '#808080', weight: 1, fillOpacity: 0}
    const purpleOptions = {color: "purple", weight: 2, fillColor:"green", fillOpacity: 0.5}
    const [geojsonData, setGeojsonData] = React.useState(null);

    function handleClick(){
        console.log("She doesn't even go here")
    }
    function getColour(score){
        const number=score.data[0].score
          // Define the hue and saturation for the heatmap
        const hue = number+230; // PURPLE!!!
        const saturation = 100;

        // Calculate the lightness based on the value, minValue, and maxValue
        const lightness = 90-(number/2);
        return `hsl(${hue}, ${100}%, ${lightness}%)`

    }
    

    const polygons=geodata.features.map((feature, idx) => {
        var path
        var click
        var score=props.scores.find(score => score.id === feature.properties.location_id)
        if (score){
            path= {color: "purple", weight: 2, fillColor:getColour(score), fillOpacity: 0.8}
            click= () => props.buildlist(feature)
        }
        else{
            path=defaultOptions
            click= handleClick
        }

        return feature.geometry.coordinates.map((polygon, polygonIndex) => {
            return(
            <Polygon
                key={`${idx}-${polygonIndex}`}
                id={feature.properties.location_id}
                positions={polygon[0].map(coord => [coord[1], coord[0]])} // swap lat and lng
                pathOptions={path}
                eventHandlers={{
                    click: click
                }}
            />)
            });
    })
    //console.log("Polygons", polygons)



    

    /*

def get_color_for_location_id(location_id, colormap, min_val, max_val):
    # Normalize the location_id value between 0 and 1
    normalized_value = (location_id - min_val) / (max_val - min_val)
    
    # Get the color from the colormap "Blues_r" at the normalized value
    rgba_color = colormap(normalized_value)

    # Convert the RGBA color to a hex color representation
    hex_color = "#{:02x}{:02x}{:02x}".format(int(rgba_color[2] * 255), int(rgba_color[1] * 255), int(rgba_color[0] * 255))
    
    return hex_color



        const [scoredPolygons, setScoredPolygons] = React.useState(polygons)

    React.useEffect(function(){
        setScoredPolygons(

        polygons.map(polygon=> {
            if (props.scores.some(score=> score.id === polygon[0].props.id)){
                console.log("Should appear")
                polygon.map(index=>{
                    console.log("index is", index.props.pathOptions)
                    const path= index.props.pathOptions
                    return({...index, path:purpleOptions})
                })

            }    
            return(polygon)
        }
        )
        )
    }, [props.score])

    console.log("Scored Polygons", scoredPolygons)

        for (let polygon of polygons){

        if (props.scores.some(score=> score.id === polygon[0].props.id)){
            polygon[0].props.pathOptions={purpleOptions}
        }
    }
for (let object of employees_data) {
    if (object.employee_id === 2) {
        object.employee_name = "Anthony";
    }
}
    const items=places.map(item=> {
      return {id:item.id, data:item.data.filter(datum => search.times.includes(datum.time))}
    })

    const harlem2=[[ -73.927185147891819, 40.797349896890118 ], [ -73.9273548544178, 40.797316580786315 ], [ -73.927346922527391, 40.79729390212043 ], [ -73.927671226208574, 40.797217014266245 ], [ -73.927706941270628, 40.797298663882124 ], [ -73.927382636244957, 40.797377063580484 ], [ -73.927366756606517, 40.797346820344757 ], [ -73.927202997851595, 40.7973867478999 ], [ -73.927185147891819, 40.797349896890118 ]]
            
    <Polygon
             pathOptions={purpleOptions}
             positions={harlem2.map(coord => [coord[1], coord[0]])}
             eventHandlers={{click: ()=> props.buildlist(location, 4)}}
        />
    // const polygons=props.data.map(location=>{
    //     return(
    //         <Polygon
    //         key={location.id}
    //         pathOptions={purpleOptions}
    //         positions={location.coordinates}
    //         eventHandlers={{click: ()=> props.buildlist(location)}}
    //         />
    //     )})

    React.useEffect(() => {
        fetch('/assets/manhattan_taxi_zones.geojson')
            .then(res => res.json())
            .then(data => setGeojsonData(data));
    }, []);

    {geojsonData && geojsonData.features.map((feature, idx) => {
        return feature.geometry.coordinates.map((polygon, polygonIndex) => (
            <Polygon
                key={`${idx}-${polygonIndex}`}
                positions={polygon[0].map(coord => [coord[1], coord[0]])} // swap lat and lng
                // pathOptions={style}
                eventHandlers={{
                    click: () => props.buildlist(feature)
                }}
            />
        ));
    })}
    */


    return (
        <div className="Map--div">
            <MapContainer center={[40.7831, -73.9712]} zoom={13} scrollWheelZoom={true}>
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                <Marker position={marker}>
                    <Popup>
                        pop six squish uh-uh cicero lipshitz
                    </Popup>
                </Marker>
                {polygons}
            </MapContainer>
        </div>)
}