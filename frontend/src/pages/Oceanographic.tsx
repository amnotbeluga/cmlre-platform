import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { api } from '../api/client';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Oceanographic = () => {
  const [sensors, setSensors] = useState<any[]>([]);
  const [activeSensor, setActiveSensor] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSensors = async () => {
      try {
        const response = await api.getStations({});
        setSensors(response.data);
        if (response.data.length > 0) {
          setActiveSensor(response.data[0]);
        }
      } catch (err) {
        console.error("Failed to fetch stations", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSensors();
  }, []);

  if (loading || !activeSensor) {
    return <div style={{ color: 'var(--text-secondary)' }}>Loading telemetry data...</div>;
  }

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px', height: 'calc(100vh - 64px)' }}>
      
      <header>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Oceanographic Telemetry</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Live spatial monitoring of physical oceanographic parameters.</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '3fr 1fr', gap: '24px', flex: 1, minHeight: 0 }}>
        

        <div className="glass-panel" style={{ padding: '8px', overflow: 'hidden', position: 'relative' }}>
          <MapContainer 
            center={[13.0, 80.0]} 
            zoom={5} 
            style={{ height: '100%', width: '100%', borderRadius: '12px' }}
            scrollWheelZoom={true}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
            
            {sensors.map(sensor => (
              <CircleMarker 
                key={sensor.id}
                center={[sensor.lat, sensor.lng]}
                radius={8}
                pathOptions={{ 
                  color: sensor.status === 'Active' ? 'var(--accent-primary)' : sensor.status === 'Warning' ? '#f59e0b' : '#ef4444',
                  fillColor: sensor.status === 'Active' ? 'var(--accent-primary)' : sensor.status === 'Warning' ? '#f59e0b' : '#ef4444',
                  fillOpacity: 0.7 
                }}
                eventHandlers={{
                  click: () => setActiveSensor(sensor),
                }}
              >
                <Popup className="custom-popup">
                  <strong style={{ color: '#000' }}>{sensor.name}</strong><br/>
                  SST: {sensor.temp}°C
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>


        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px', overflowY: 'auto' }}>
          <div>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600, color: 'var(--text-primary)' }}>{activeSensor.name}</h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px' }}>
              <div style={{ 
                width: '8px', height: '8px', borderRadius: '50%', 
                background: activeSensor.status === 'Active' ? '#10b981' : activeSensor.status === 'Warning' ? '#f59e0b' : '#ef4444' 
              }}></div>
              <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{activeSensor.status}</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Sea Surface Temp</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--text-accent)' }}>{activeSensor.temp}°C</div>
            </div>
            
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Salinity (PSU)</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--accent-secondary)' }}>{activeSensor.salinity}</div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Coordinates</div>
              <div style={{ fontSize: '1rem', fontWeight: 500 }}>{activeSensor.lat.toFixed(2)}°N, {activeSensor.lng.toFixed(2)}°E</div>
            </div>
          </div>
          
          <button style={{ 
            marginTop: 'auto',
            padding: '12px',
            background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'opacity 0.2s'
          }}>
            Download History
          </button>
        </div>

      </div>
    </div>
  );
};

export default Oceanographic;
