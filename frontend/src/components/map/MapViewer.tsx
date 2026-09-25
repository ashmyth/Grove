import React, { useEffect, useRef } from "react";
import L from "leaflet";
import type { ParcelFeatureCollection, CanalLineFeatureCollection, ParcelFeature } from "../../types";

interface MapViewerProps {
  parcels: ParcelFeatureCollection | null;
  canalNetwork: CanalLineFeatureCollection | null;
  selectedParcelId: string | null;
  onSelectParcel: (id: string) => void;
  activeLayer: "stress" | "optical" | "sar" | "thermal";
  onLayerChange: (layer: "stress" | "optical" | "sar" | "thermal") => void;
}

export const MapViewer: React.FC<MapViewerProps> = ({
  parcels,
  canalNetwork,
  selectedParcelId,
  onSelectParcel,
  activeLayer,
  onLayerChange,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const parcelsLayerRef = useRef<L.GeoJSON | null>(null);
  const canalLayerRef = useRef<L.GeoJSON | null>(null);

  // Initialize Map
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center: [30.710, 76.870],
      zoom: 14,
      zoomControl: false,
    });

    // High-resolution satellite basemap with attribution
    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Esri, Maxar, Earthstar Geographics",
        maxZoom: 19,
      }
    ).addTo(map);

    L.control.zoom({ position: "topright" }).addTo(map);

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Update Canal Lines
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map || !canalNetwork) return;

    if (canalLayerRef.current) {
      canalLayerRef.current.remove();
    }

    const layer = L.geoJSON(canalNetwork as any, {
      style: (feature) => {
        const isMain = feature?.properties?.type === "Main Canal";
        return {
          color: isMain ? "#38bdf8" : "#0284c7",
          weight: isMain ? 4 : 2.5,
          opacity: 0.95,
          dashArray: isMain ? undefined : "5, 5",
        };
      },
      onEachFeature: (feature, layer) => {
        layer.bindTooltip(
          `<strong>${feature.properties.name}</strong><br/>Type: ${feature.properties.type}`,
          { sticky: true }
        );
      },
    }).addTo(map);

    canalLayerRef.current = layer;
  }, [canalNetwork]);

  // Update Parcels
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map || !parcels) return;

    if (parcelsLayerRef.current) {
      parcelsLayerRef.current.remove();
    }

    const getParcelColor = (props: any) => {
      if (activeLayer === "sar") {
        return props.stress_score > 0.7 ? "#f97316" : "#06b6d4";
      }
      if (activeLayer === "thermal") {
        return props.stress_score > 0.6 ? "#ef4444" : "#eab308";
      }
      // Stress Default
      switch (props.stress_level) {
        case "Severe":
          return "#ef4444";
        case "Moderate":
          return "#eab308";
        case "Mild":
          return "#84cc16";
        case "Normal":
        default:
          return "#10b981";
      }
    };

    const layer = L.geoJSON(parcels as any, {
      style: (feature) => {
        const isSelected = feature?.properties?.id === selectedParcelId;
        return {
          fillColor: getParcelColor(feature?.properties),
          weight: isSelected ? 3 : 1.5,
          opacity: 1,
          color: isSelected ? "#ffffff" : "rgba(255, 255, 255, 0.4)",
          fillOpacity: isSelected ? 0.75 : 0.55,
        };
      },
      onEachFeature: (feature: ParcelFeature, layer) => {
        const p = feature.properties;
        layer.on({
          click: () => onSelectParcel(p.id),
        });
        layer.bindTooltip(
          `<div>
            <div style="font-weight:700; font-size:12px;">${p.block_name}</div>
            <div style="font-size:11px; color:#94a3b8;">${p.id} • ${p.crop_type} (${p.stage})</div>
            <div style="font-size:11px; margin-top:3px;">Stress: <strong>${p.stress_level}</strong> (${(p.stress_score * 100).toFixed(0)}%)</div>
            <div style="font-size:11px;">Deficit: <strong>${p.deficit_m3_ha}</strong> m³/ha</div>
          </div>`,
          { sticky: true }
        );
      },
    }).addTo(map);

    parcelsLayerRef.current = layer;
  }, [parcels, selectedParcelId, activeLayer, onSelectParcel]);

  return (
    <div style={{ flex: 1, position: "relative", height: "100%", overflow: "hidden" }}>
      {/* Leaflet DOM container */}
      <div ref={mapContainerRef} style={{ width: "100%", height: "100%" }} />

      {/* Floating Layer Switcher Controls */}
      <div
        style={{
          position: "absolute",
          top: "var(--space-md)",
          left: "var(--space-md)",
          zIndex: 1000,
          display: "flex",
          gap: "var(--space-2xs)",
          backgroundColor: "var(--bg-panel)",
          padding: "var(--space-2xs)",
          borderRadius: "8px",
          border: "1px solid var(--border-subtle)",
          boxShadow: "var(--shadow-panel)",
        }}
      >
        {(["stress", "optical", "sar", "thermal"] as const).map((layer) => (
          <button
            key={layer}
            onClick={() => onLayerChange(layer)}
            style={{
              padding: "6px 12px",
              borderRadius: "6px",
              fontSize: "11px",
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: "0.03em",
              border: "none",
              cursor: "pointer",
              backgroundColor: activeLayer === layer ? "var(--accent-brand)" : "transparent",
              color: activeLayer === layer ? "#ffffff" : "var(--text-muted)",
              transition: "all 0.15s ease",
            }}
          >
            {layer === "stress" ? "Crop Stress" : layer === "optical" ? "S2 NDVI" : layer === "sar" ? "S1 SAR Moisture" : "L8 Thermal"}
          </button>
        ))}
      </div>

      {/* Floating Legend */}
      <div
        style={{
          position: "absolute",
          bottom: "var(--space-md)",
          left: "var(--space-md)",
          zIndex: 1000,
          backgroundColor: "var(--bg-panel)",
          padding: "var(--space-sm) var(--space-md)",
          borderRadius: "8px",
          border: "1px solid var(--border-subtle)",
          boxShadow: "var(--shadow-panel)",
          fontSize: "11px",
        }}
      >
        <div style={{ fontWeight: 700, marginBottom: "var(--space-2xs)", color: "var(--text-dim)", textTransform: "uppercase", fontSize: "10px", letterSpacing: "0.05em" }}>
          Stress Severity (CMSI)
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2xs)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#ef4444" }} />
            <span>Severe Water Deficit (&gt; 0.75)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#eab308" }} />
            <span>Moderate Stress (0.50 - 0.75)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#84cc16" }} />
            <span>Mild Stress (0.35 - 0.50)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#10b981" }} />
            <span>Healthy Crop / Low Deficit (&lt; 0.35)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "var(--space-2xs)", paddingTop: "var(--space-2xs)", borderTop: "1px dashed var(--border-subtle)" }}>
            <span style={{ width: "14px", height: "3px", backgroundColor: "#38bdf8" }} />
            <span>Canal Distribution Network</span>
          </div>
        </div>
      </div>
    </div>
  );
};
