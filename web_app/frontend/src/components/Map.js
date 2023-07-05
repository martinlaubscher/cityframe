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
        <MapContainer center={[40.7831, -73.9712]} zoom={13} scrollWheelZoom={false} >
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




/*
            <Polygon pathOptions={purpleOptions} positions={polygon} eventHandlers={{click: ()=> handleClick(polygon)}} />

    const polygon = [
      [40.7831, -73.9712],
      [40.7931, -73.9712],
      [40.7831, -73.9812]
    ]


    function ClickMap (){
        useMapEvents({
            click() {
            console.log("clicked")
            }})
    }

// Create the map
var map = L.map('map').setView([79, -100], 5);

// Set up the OSM layer
L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
    {maxZoom: 18}).addTo(map);

//Handle click on polygon
var onPolyClick = function(event){
    //callFancyboxIframe('flrs.html')
    var label = event.target.options.label;
    var content = event.target.options.popup;
    var otherStuff = event.target.options.otherStuff;
    alert("Clicked on polygon with label:" +label +" and content:" +content +". Also otherStuff set to:" +otherStuff);
};

//Create polygon
var popup_flor ="MyLabel";
var content_flor ="MyContent";
var poly = new L.Polygon([
        [79.07181, -100.63477], 
        [79.06348, -90.43945], 
        [77.52312, -90.52734], 
        [77.50412, -94.21875], 
        [77.41825, -94.35059], 
        [77.40868, -96.72363], 
        [77.51362, -96.81152], 
        [77.53261, -100.63477], 
        [79.07181, -100.63477]
  ], {'label': popup_flor, 'popup': content_flor, 'otherStuff': 'abc123'});
poly.on('click', onPolyClick);

//Add polygon to map
poly.addTo(map);    

    function Click(){
        useMapEvents({
            click() {
            console.log("Clicked")
        }
    })}




render(
  <MapContainer center={center} zoom={13} scrollWheelZoom={false}>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <Circle center={center} pathOptions={fillBlueOptions} radius={200} />
    <CircleMarker center={[51.51, -0.12]} pathOptions={redOptions} radius={20}>
      <Popup>Popup in CircleMarker</Popup>
    </CircleMarker>
    <Polyline pathOptions={limeOptions} positions={polyline} />
    <Polyline pathOptions={limeOptions} positions={multiPolyline} />

    <Polygon pathOptions={purpleOptions} positions={polygon} />
    <Polygon pathOptions={purpleOptions} positions={multiPolygon} />
    <Rectangle bounds={rectangle} pathOptions={blackOptions} />
  </MapContainer>,
)










    //var map = L.map('map').setView([51.505, -0.09], 13);
<div id="map" style="height: 500px; background-color: aqua;"></div>
    
    
<script>
var map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
maxZoom: 19,
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


var polygon = L.polygon([
[51.509, -0.08],
[51.503, -0.06],
[51.51, -0.047],
]).addTo(map);

var polygon = L.polygon([
[51.609, -0.18],
[51.603, -0.16],
[51.61, -0.147],
]).addTo(map);

</script>
*/
