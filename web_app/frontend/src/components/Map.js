import { MapContainer, TileLayer, Marker, Popup, Polygon} from 'react-leaflet'
import data from '../locationjunk'

export default function Map(){
    

    function handleClick(e){
        console.log(data, e)
    }
    const purpleOptions = { color: 'purple' }

    const polygons=data.map(location=>{
        return(
            <Polygon
            key={location.id}
            pathOptions={purpleOptions}
            positions={location.coordinates}
            eventHandlers={{click: ()=> handleClick(location.name)}}
            />
        )}
        )
    




    return(
    <div className="Map--div" >
        <p>Map goes here</p>
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
        <p>Ta da</p>
    </div>)
}
