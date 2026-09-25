export type ReachType = "head" | "middle" | "tail";
export type StressLevel = "Normal" | "Mild" | "Moderate" | "Severe";

export interface CanalAdvisoryItem {
  id: string;
  block_name: string;
  reach: ReachType;
  crop_type: string;
  stage: string;
  deficit_m3_ha: number;
  discharge_cumecs: number;
  stress_level: StressLevel;
}

export interface PixelTimeseriesData {
  dates: string[];
  doy: number[];
  ndvi_raw: number[];
  ndvi_smoothed: number[];
  smi_sar: number[];
  lst_anomaly: number[];
}

export interface CommandOverview {
  cycle_days: number;
  total_area_ha: number;
  total_deficit_m3: number;
  total_recommended_discharge_cumecs: number;
  severe_stress_parcels_count: number;
  reaches_count: {
    head: number;
    middle: number;
    tail: number;
  };
}

export interface ParcelProperties {
  id: string;
  block_name: string;
  reach: ReachType;
  crop_type: string;
  stage: string;
  stress_level: StressLevel;
  stress_score: number;
  deficit_m3_ha: number;
  recommended_discharge: number;
  area_ha: number;
  ndvi?: number;
  smi_sar?: number;
  lst_anomaly?: number;
  farmer?: string;
  ai_predicted_crop?: string;
  ai_confidence?: number;
  ai_class_probabilities?: Record<string, number>;
  features_used?: {
    s2_ndvi: number;
    s1_smi: number;
    sar_vh_db: number;
    lst_anomaly: number;
  };
}

export interface ModelDiagnostics {
  model_name: string;
  training_samples: number;
  test_samples: number;
  accuracy: number;
  macro_f1: number;
  macro_precision: number;
  macro_recall: number;
  confusion_matrix: number[][];
  class_names: string[];
  per_class_metrics: Record<string, {
    precision: number;
    recall: number;
    f1_score: number;
    support: number;
  }>;
  top_features: Array<{
    feature: string;
    importance: number;
  }>;
  status?: string;
  message?: string;
}

export interface ParcelFeature {
  type: "Feature";
  id: string;
  properties: ParcelProperties;
  geometry: {
    type: "Polygon";
    coordinates: number[][][];
  };
}

export interface ParcelFeatureCollection {
  type: "FeatureCollection";
  features: ParcelFeature[];
}

export interface CanalLineFeature {
  type: "Feature";
  properties: {
    name: string;
    type: string;
    flow_direction: string;
  };
  geometry: {
    type: "LineString";
    coordinates: number[][];
  };
}

export interface CanalLineFeatureCollection {
  type: "FeatureCollection";
  features: CanalLineFeature[];
}

export interface AnalysisInputPayload {
  command_area_id: string;
  start_date: string;
  end_date: string;
  available_discharge_cumecs: number;
  custom_geojson?: any;
}

export interface AnalysisRunResponse {
  status: "success" | "error";
  message: string;
  overview: CommandOverview;
  parcels: ParcelFeatureCollection;
  advisories: CanalAdvisoryItem[];
  canal_network: CanalLineFeatureCollection;
}
