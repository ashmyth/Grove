import type {
  CanalAdvisoryItem,
  PixelTimeseriesData,
  CommandOverview,
  ParcelFeatureCollection,
  CanalLineFeatureCollection,
  AnalysisInputPayload,
  AnalysisRunResponse
} from "../types";

const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function fetchCommandOverview(): Promise<CommandOverview> {
  const res = await fetch(`${API_BASE}/overview`);
  if (!res.ok) throw new Error("Failed to fetch command overview");
  return res.json();
}

export async function fetchCanalAdvisory(
  reach?: string,
  stress?: string
): Promise<CanalAdvisoryItem[]> {
  const params = new URLSearchParams();
  if (reach && reach !== "all") params.append("reach", reach);
  if (stress && stress !== "all") params.append("stress", stress);
  
  const url = `${API_BASE}/canal-advisory?${params.toString()}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch canal advisories");
  return res.json();
}

export async function fetchParcelsGeoJSON(): Promise<ParcelFeatureCollection> {
  const res = await fetch(`${API_BASE}/parcels/geojson`);
  if (!res.ok) throw new Error("Failed to fetch parcels GeoJSON");
  return res.json();
}

export async function fetchCanalNetworkGeoJSON(): Promise<CanalLineFeatureCollection> {
  const res = await fetch(`${API_BASE}/canal/network`);
  if (!res.ok) throw new Error("Failed to fetch canal network");
  return res.json();
}

export async function fetchPixelTimeseries(
  parcelId: string
): Promise<PixelTimeseriesData> {
  const res = await fetch(`${API_BASE}/pixel-timeseries?parcel_id=${encodeURIComponent(parcelId)}`);
  if (!res.ok) throw new Error("Failed to fetch pixel timeseries");
  return res.json();
}

export async function runCommandAnalysis(
  payload: AnalysisInputPayload
): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/run-analysis`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to run pipeline analysis");
  return res.json();
}
