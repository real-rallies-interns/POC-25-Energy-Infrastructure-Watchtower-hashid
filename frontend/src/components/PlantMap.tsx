"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix Leaflet marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

interface PlantMapProps {
  plants: any;
}

export default function PlantMap({ plants }: PlantMapProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="h-full w-full flex items-center justify-center bg-obsidian text-slate-500">Loading Map...</div>;
  }

  const getFuelColor = (fuelType: string) => {
    switch (fuelType) {
      case "Nuclear": return "#818CF8"; // Indigo
      case "Hydro": return "#38BDF8"; // Cyan
      case "Solar": return "#FCD34D"; // Yellow
      case "Wind": return "#A7F3D0"; // Green
      case "Gas": return "#FCA5A5"; // Red
      case "Coal": return "#9CA3AF"; // Gray
      default: return "#ffffff";
    }
  };

  const createLocationIcon = (fuelType: string, status: string) => {
    const color = getFuelColor(fuelType);
    const isOutage = status === "Outage";
    
    return L.divIcon({
      className: "custom-location-icon",
      html: `
        <div style="position: relative; width: 30px; height: 30px;">
          <svg viewBox="0 0 24 24" width="30" height="30" fill="${color}" style="filter: drop-shadow(0 0 4px ${color}88);">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
          ${isOutage ? `<div style="position: absolute; top: 0; left: 0; width: 30px; height: 30px; border: 2px solid #ef4444; border-radius: 50%; animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;"></div>` : ""}
        </div>
      `,
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -30],
    });
  };

  return (
    <MapContainer
      center={[39.8283, -98.5795]}
      zoom={4}
      style={{ height: "100%", width: "100%", background: "#030712" }}
      zoomControl={false}
    >
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
      />
      {plants?.features?.map((feature: any) => {
        const p = feature.properties;
        const [lon, lat] = feature.geometry.coordinates;
        return (
          <Marker
            key={p.id}
            position={[lat, lon]}
            icon={createLocationIcon(p.fuel_type, p.status)}
          >
            <Popup className="bg-navy border border-slate-800 text-white rounded-md glassmorphism p-2">
              <div className="flex flex-col gap-1 text-sm">
                <strong className="text-cyan-glow uppercase tracking-tighter">{p.name}</strong>
                <div className="flex items-center gap-2 mt-1">
                  <div className="w-2 h-2 rounded-full" style={{ background: getFuelColor(p.fuel_type) }}></div>
                  <span className="text-xs text-slate-300">{p.fuel_type}</span>
                </div>
                <div className="text-xs text-slate-400">Capacity: <span className="text-white">{p.capacity_mw} MW</span></div>
                <div className={`text-[10px] font-bold mt-1 px-2 py-0.5 rounded border inline-block w-fit ${
                  p.status === "Outage" ? "bg-red-950/40 text-red-400 border-red-900/50" : 
                  p.status === "Maintenance" ? "bg-yellow-950/40 text-yellow-400 border-yellow-900/50" : 
                  "bg-green-950/40 text-green-400 border-green-900/50"
                }`}>
                  {p.status.toUpperCase()}
                </div>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
