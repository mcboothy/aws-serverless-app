import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

const Map = () => {
    const position = [8.1386, 5.1026];
    const zoomLevel = 15;

    return (
        <MapContainer zoom={zoomLevel} center={position} scrollWheelZoom={true} style={{width: '100%', height: '100vh'}}>
            <TileLayer url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' />

            <Marker position={position}>
                <Popup>
                    Omu-Aran the Head Post of Igbomina land,
                    is a town in the Nigerian state of Kwara.
                    It originated from Ife and currently the local
                    government headquarters of Irepodun local government.
                </Popup>
            </Marker>
        </MapContainer>
    );
}


export default Map;