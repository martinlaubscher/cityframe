import {MapContainer, TileLayer, Marker, Popup, Polygon} from 'react-leaflet'
import "./MapBackground.css"
import React from 'react'

import geodata from '../dummydata/geodata'

export default function Map(props) {
    const [marker, setMarker] = React.useState([40.7831, -73.9712])
    const purpleOptions = {color: 'purple'}
    const [geojsonData, setGeojsonData] = React.useState(null);

    const polygons=geodata.features.map((feature, idx) => {
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
    })

    // const polygons=props.data.map(location=>{
    //     return(
    //         <Polygon
    //         key={location.id}
    //         pathOptions={purpleOptions}
    //         positions={location.coordinates}
    //         eventHandlers={{click: ()=> props.buildlist(location)}}
    //         />
    //     )})
/*
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