import { useState, useEffect } from "react";
import { Header } from "./components/layout/Header";
import { CanalTelemetry } from "./components/telemetry/CanalTelemetry";
import { MapViewer } from "./components/map/MapViewer";
import { AnalyticsDrawer } from "./components/analytics/AnalyticsDrawer";
import {
  fetchCommandOverview,
  fetchCanalAdvisory,
  fetchParcelsGeoJSON,
  fetchCanalNetworkGeoJSON,
} from "./services/api";
import type {
  CommandOverview,
  CanalAdvisoryItem,
  ParcelFeatureCollection,
  CanalLineFeatureCollection,
  ReachType,
} from "./types";

export function App() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [overview, setOverview] = useState<CommandOverview | null>(null);
  const [advisories, setAdvisories] = useState<CanalAdvisoryItem[]>([]);
  const [parcels, setParcels] = useState<ParcelFeatureCollection | null>(null);
  const [canalNetwork, setCanalNetwork] = useState<CanalLineFeatureCollection | null>(null);
  const [selectedParcelId, setSelectedParcelId] = useState<string | null>("PARCEL-C309");
  const [reachFilter, setReachFilter] = useState<ReachType | "all">("all");
  const [activeLayer, setActiveLayer] = useState<"stress" | "optical" | "sar" | "thermal">("stress");

  // Load telemetry & geospatial data
  const loadData = async () => {
    try {
      const [ov, adv, parc, canal] = await Promise.all([
        fetchCommandOverview(),
        fetchCanalAdvisory(reachFilter),
        fetchParcelsGeoJSON(),
        fetchCanalNetworkGeoJSON(),
      ]);
      setOverview(ov);
      setAdvisories(adv);
      setParcels(parc);
      setCanalNetwork(canal);
    } catch (err) {
      console.error("Error loading Grove command data:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, [reachFilter]);

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    if (next === "light") {
      document.documentElement.setAttribute("data-theme", "light");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  };

  const selectedParcel = parcels?.features.find((f) => f.properties.id === selectedParcelId) || null;

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", overflow: "hidden" }}>
      {/* Global Command Header */}
      <Header
        theme={theme}
        onToggleTheme={toggleTheme}
        onRefresh={loadData}
        onExport={() => alert("Exporting 8-Day Canal Command Advisory (PDF/CSV)...")}
        cycleDays={overview?.cycle_days || 8}
      />

      {/* 3-Panel GIS Command Deck */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Panel 1: Canal Telemetry & Advisory Sidebar */}
        <CanalTelemetry
          overview={overview}
          advisories={advisories}
          selectedParcelId={selectedParcelId}
          onSelectParcel={(id) => setSelectedParcelId(id)}
          reachFilter={reachFilter}
          onFilterReach={(reach) => setReachFilter(reach)}
        />

        {/* Panel 2: Interactive Leaflet GIS Satellite Map */}
        <MapViewer
          parcels={parcels}
          canalNetwork={canalNetwork}
          selectedParcelId={selectedParcelId}
          onSelectParcel={(id) => setSelectedParcelId(id)}
          activeLayer={activeLayer}
          onLayerChange={(layer) => setActiveLayer(layer)}
        />

        {/* Panel 3: Phenology & Timeseries Analytics Drawer */}
        <AnalyticsDrawer
          selectedParcel={selectedParcel}
          onClose={() => setSelectedParcelId(null)}
        />
      </div>
    </div>
  );
}

export default App;
