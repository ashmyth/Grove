import React, { useEffect, useRef } from "react";
import L from "leaflet";
import type { ParcelFeatureCollection, CanalLineFeatureCollection, ParcelFeature } from "../../types";

interface MapViewerProps {
  parcels: ParcelFeatureCollection | null;
  canalNetwork: CanalLineFeatureCollection | null;
  selectedParcelId: string | null;
  onSelectParcel: (id: string) => void;
  activeLayer: "stress" | "crop" | "optical" | "sar" | "thermal";
  onLayerChange: (layer: "stress" | "crop" | "optical" | "sar" | "thermal") => void;
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
      if (activeLayer === "crop") {
        const crop = props.ai_predicted_crop || props.crop_type || "";
        if (crop.includes("Paddy") || crop.includes("Rice")) return "#0284c7"; // Blue
        if (crop.includes("Cotton")) return "#f59e0b"; // Warm Amber
        if (crop.includes("Maize")) return "#84cc16"; // Lime Green
        if (crop.includes("Sugarcane")) return "#10b981"; // Emerald
        return "#eab308"; // Golden Wheat / Mustard
      }
      if (activeLayer === "optical") {
        const ndvi = props.ndvi ?? 0.6;
        if (ndvi >= 0.75) return "#15803d";
        if (ndvi >= 0.60) return "#22c55e";
        if (ndvi >= 0.45) return "#eab308";
        return "#f97316";
      }
      if (activeLayer === "sar") {
        const smi = props.smi_sar ?? 0.5;
        if (smi >= 0.60) return "#0284c7";
        if (smi >= 0.40) return "#06b6d4";
        if (smi >= 0.25) return "#f59e0b";
        return "#ef4444";
      }
      if (activeLayer === "thermal") {
        const lst = props.lst_anomaly ?? 0.0;
        if (lst < 0.0) return "#06b6d4";
        if (lst <= 1.5) return "#eab308";
        if (lst <= 3.0) return "#f97316";
        return "#dc2626";
      }
      // Stress Default (CMSI)
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
          weight: isSelected ? 3.5 : 1.5,
          opacity: 1,
          color: isSelected ? "#ffffff" : "rgba(255, 255, 255, 0.45)",
          fillOpacity: isSelected ? 0.85 : 0.65,
        };
      },
      onEachFeature: (feature: ParcelFeature, layer) => {
        const p = feature.properties;
        layer.on({
          click: () => onSelectParcel(p.id),
        });
        layer.bindTooltip(
          `<div style="font-family: inherit; line-height: 1.4;">
            <div style="font-weight:700; font-size:12px; color:#f8fafc; border-bottom:1px solid #334155; padding-bottom:3px; margin-bottom:4px;">
              ${p.block_name}
            </div>
            <div style="font-size:11px; color:#cbd5e1; font-weight:600;">
              ${p.id} • ${p.crop_type}
            </div>
            <div style="font-size:11px; color:#38bdf8; font-weight:600; margin-top:2px;">
              AI Classified: <strong>${p.ai_predicted_crop ?? p.crop_type}</strong> ${p.ai_confidence ? `(${Math.round(p.ai_confidence * 100)}% conf)` : ''}
            </div>
            <div style="font-size:11px; color:#94a3b8; margin-top:2px;">
              Stage: <span style="color:#e2e8f0;">${p.stage}</span> • Area: <span style="color:#e2e8f0;">${p.area_ha} ha</span>
            </div>
            <div style="display:flex; gap:8px; margin-top:4px; font-size:10px; background:#0f172a; padding:3px 6px; border-radius:4px;">
              <span>NDVI: <strong>${p.ndvi ?? 0.65}</strong></span>
              <span>SMI: <strong>${p.smi_sar ?? 0.45}</strong></span>
              <span>ΔT: <strong>${p.lst_anomaly ? (p.lst_anomaly > 0 ? '+' : '') + p.lst_anomaly + '°C' : '0.0°C'}</strong></span>
            </div>
            <div style="font-size:11px; margin-top:4px; color:#f8fafc;">
              Water Deficit: <strong style="color:#f87171;">${p.deficit_m3_ha} m³/ha</strong>
            </div>
            <div style="font-size:11px; color:#38bdf8;">
              Recommended Release: <strong>${p.recommended_discharge} m³/s</strong>
            </div>
          </div>`,
          { sticky: true }
        );
      },
    }).addTo(map);

    // Auto-fit bounds to agricultural parcels
    try {
      const bounds = layer.getBounds();
      if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
      }
    } catch (e) {
      console.warn("Could not fit bounds to parcels:", e);
    }

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

      {/* Floating Dynamic Legend */}
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
          minWidth: "220px",
        }}
      >
        {activeLayer === "stress" && (
          <>
            <div style={{ fontWeight: 700, marginBottom: "var(--space-2xs)", color: "var(--text-dim)", textTransform: "uppercase", fontSize: "10px", letterSpacing: "0.05em" }}>
              Crop Stress Severity (CMSI)
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
            </div>
          </>
        )}

        {activeLayer === "optical" && (
          <>
            <div style={{ fontWeight: 700, marginBottom: "var(--space-2xs)", color: "var(--text-dim)", textTransform: "uppercase", fontSize: "10px", letterSpacing: "0.05em" }}>
              Sentinel-2 MSI (NDVI Index)
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2xs)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#15803d" }} />
                <span>Dense Healthy Canopy (≥ 0.75)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#22c55e" }} />
                <span>Active Vegetative Growth (0.60 - 0.75)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#eab308" }} />
                <span>Emergence / Moderate Biomass (0.45 - 0.60)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#f97316" }} />
                <span>Low Canopy / Fallow (&lt; 0.45)</span>
              </div>
            </div>
          </>
        )}

        {activeLayer === "sar" && (
          <>
            <div style={{ fontWeight: 700, marginBottom: "var(--space-2xs)", color: "var(--text-dim)", textTransform: "uppercase", fontSize: "10px", letterSpacing: "0.05em" }}>
              Sentinel-1 SAR Topsoil Moisture (SMI)
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2xs)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#0284c7" }} />
                <span>Saturated / Sluice Irrigated (≥ 0.60)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#06b6d4" }} />
                <span>Adequate Rootzone Moisture (0.40 - 0.60)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#f59e0b" }} />
                <span>Moisture Depleted (0.25 - 0.40)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#ef4444" }} />
                <span>Acute Soil Drought (&lt; 0.25)</span>
              </div>
            </div>
          </>
        )}

        {activeLayer === "thermal" && (
          <>
            <div style={{ fontWeight: 700, marginBottom: "var(--space-2xs)", color: "var(--text-dim)", textTransform: "uppercase", fontSize: "10px", letterSpacing: "0.05em" }}>
              Landsat-8 Thermal Anomaly (ΔT °C)
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2xs)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#dc2626" }} />
                <span>Thermal Spike / Stomatal Shutdown (&gt; +3.0°C)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#f97316" }} />
                <span>Canopy Temperature Elevated (+1.5 - +3.0°C)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#eab308" }} />
                <span>Normal Transpiration Range (0.0 - +1.5°C)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "10px", height: "10px", borderRadius: "2px", backgroundColor: "#06b6d4" }} />
                <span>Cool Canopy / High Transpiration (&lt; 0.0°C)</span>
              </div>
            </div>
          </>
        )}

        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "var(--space-2xs)", paddingTop: "var(--space-2xs)", borderTop: "1px dashed var(--border-subtle)" }}>
          <span style={{ width: "14px", height: "3px", backgroundColor: "#38bdf8" }} />
          <span>Canal Distribution Network</span>
        </div>
      </div>
    </div>
  );
};
