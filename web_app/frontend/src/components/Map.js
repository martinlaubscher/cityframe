import { MapContainer, TileLayer, Marker, Popup, Polygon} from 'react-leaflet'


export default function Map(props){

    const purpleOptions = { color: 'purple' }
    const polygons=props.data.map(location=>{
        return(
            <Polygon
            key={location.id}
            pathOptions={purpleOptions}
            positions={location.coordinates}
            eventHandlers={{click: ()=> props.buildlist(location)}}
            />
        )}
        )
    




    return(
    <div className="Map--div" >
        <MapContainer center={[40.7831, -73.9712]} zoom={13} scrollWheelZoom={true} >
            <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
            <Marker position={[40.7831, -73.9712]} >
                <Popup>
                    Manhattan!
                </Popup>
            </Marker>
            {polygons}
        </MapContainer>
    </div>)
}
