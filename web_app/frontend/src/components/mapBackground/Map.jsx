import { MapContainer, TileLayer, Marker, Popup, Polygon} from 'react-leaflet'
import "./MapBackground.css"
import React from 'react'

export default function Map(props){
    //const [stateData, setStateData]=React.useState(dynamic)

    const [marker, setMarker]=React.useState([40.7831, -73.9712])
    const purpleOptions = { color: 'purple' }


    function handleClick(location){
        console.log(location.name)
        setMarker(location.coordinates[0])
    }

    const polygons=props.data.map(location=>{
        return(
            <Polygon
            key={location.id}
            pathOptions={purpleOptions}
            positions={location.coordinates}
            //onClick={()=> props.buildlist(location)}
            //eventHandlers={{click: ()=> handleClick(location)}}
            eventHandlers={{click: ()=> props.buildlist(location)}}
            />
        )})

    return(
    <div className="Map--div" >
        <MapContainer center={[40.7831, -73.9712]} zoom={13} scrollWheelZoom={true} >
            <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
            <Marker position={marker} >
                <Popup>
                    Manhattan!
                </Popup>
            </Marker>

            {polygons}
        </MapContainer>
    </div>)
}