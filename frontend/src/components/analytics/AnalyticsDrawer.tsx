import React, { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import type { PixelTimeseriesData, ParcelFeature } from "../../types";
import { fetchPixelTimeseries } from "../../services/api";
import { X, Activity, Thermometer } from "lucide-react";

interface AnalyticsDrawerProps {
  selectedParcel: ParcelFeature | null;
  onClose: () => void;
}

export const AnalyticsDrawer: React.FC<AnalyticsDrawerProps> = ({
  selectedParcel,
  onClose,
}) => {
  const [timeseries, setTimeseries] = useState<PixelTimeseriesData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!selectedParcel) return;
    setLoading(true);
    fetchPixelTimeseries(selectedParcel.properties.id)
      .then((data) => setTimeseries(data))
      .catch((err) => console.error("Timeseries fetch error:", err))
      .finally(() => setLoading(false));
  }, [selectedParcel]);

  if (!selectedParcel) return null;

  const props = selectedParcel.properties;
  const chartData =
    timeseries?.dates.map((date, idx) => ({
      date: date.substring(5), // MM-DD
      doy: timeseries.doy[idx],
      ndvi_raw: timeseries.ndvi_raw[idx],
      ndvi_smoothed: timeseries.ndvi_smoothed[idx],
      smi_sar: timeseries.smi_sar[idx],
      lst_anomaly: timeseries.lst_anomaly[idx],
    })) || [];

  return (
    <div
      style={{
        width: "420px",
        minWidth: "420px",
        height: "calc(100vh - 56px)",
        backgroundColor: "var(--bg-panel)",
        borderLeft: "1px solid var(--border-subtle)",
        display: "flex",
        flexDirection: "column",
        overflowY: "auto",
        zIndex: 500,
        boxShadow: "var(--shadow-panel)",
      }}
    >
      {/* Drawer Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "16px",
          borderBottom: "1px solid var(--border-subtle)",
        }}
      >
        <div>
          <span style={{ fontSize: "11px", fontWeight: 700, color: "var(--text-dim)", textTransform: "uppercase" }}>
            Parcel Earth Observation Inspector
          </span>
          <h2 style={{ fontSize: "16px", fontWeight: 700, marginTop: "2px" }}>{props.block_name}</h2>
        </div>
        <button
          onClick={onClose}
          style={{
            background: "none",
            border: "none",
            color: "var(--text-dim)",
            cursor: "pointer",
            padding: "4px",
          }}
        >
          <X size={18} />
        </button>
      </div>

      {/* Parcel Metrics Strip */}
      <div style={{ padding: "16px", borderBottom: "1px solid var(--border-subtle)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
          <div style={{ padding: "8px", background: "var(--bg-surface)", borderRadius: "6px" }}>
            <span style={{ fontSize: "10px", color: "var(--text-dim)" }}>Crop & Growth Stage</span>
            <div style={{ fontSize: "13px", fontWeight: 600 }}>
              {props.crop_type} ({props.stage})
            </div>
          </div>
          <div style={{ padding: "8px", background: "var(--bg-surface)", borderRadius: "6px" }}>
            <span style={{ fontSize: "10px", color: "var(--text-dim)" }}>Command Reach</span>
            <div style={{ fontSize: "13px", fontWeight: 600, textTransform: "capitalize" }}>
              {props.reach} Distributary
            </div>
          </div>
          <div style={{ padding: "8px", background: "var(--bg-surface)", borderRadius: "6px" }}>
            <span style={{ fontSize: "10px", color: "var(--text-dim)" }}>Irrigation Deficit</span>
            <div className="telemetry-num" style={{ fontSize: "14px", fontWeight: 700, color: "var(--stress-severe)" }}>
              {props.deficit_m3_ha} <span className="telemetry-decimal">m³/ha</span>
            </div>
          </div>
          <div style={{ padding: "8px", background: "var(--bg-surface)", borderRadius: "6px" }}>
            <span style={{ fontSize: "10px", color: "var(--text-dim)" }}>Recommended Gate Discharge</span>
            <div className="telemetry-num" style={{ fontSize: "14px", fontWeight: 700, color: "var(--accent-water)" }}>
              {props.recommended_discharge} <span className="telemetry-decimal">m³/s</span>
            </div>
          </div>
        </div>
      </div>

      {/* Multi-temporal Phenology Chart */}
      <div style={{ padding: "16px", flex: 1 }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
          <span style={{ fontSize: "12px", fontWeight: 700, color: "var(--text-main)", display: "flex", alignItems: "center", gap: "6px" }}>
            <Activity size={14} color="var(--accent-brand)" />
            Savitzky-Golay Smoothed Phenology
          </span>
          <span style={{ fontSize: "10px", color: "var(--text-dim)" }}>12-Day Sentinel Cadence</span>
        </div>

        <div style={{ height: "230px", background: "var(--bg-surface)", padding: "10px", borderRadius: "8px" }}>
          {loading ? (
            <div style={{ display: "flex", height: "100%", alignItems: "center", justifyContent: "center", fontSize: "12px", color: "var(--text-dim)" }}>
              Loading Multi-Temporal Curves...
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                <XAxis dataKey="date" stroke="var(--text-dim)" fontSize={10} />
                <YAxis domain={[0, 1]} stroke="var(--text-dim)" fontSize={10} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--bg-panel)",
                    borderColor: "var(--border-strong)",
                    fontSize: "11px",
                    borderRadius: "6px",
                  }}
                />
                <Legend iconSize={8} wrapperStyle={{ fontSize: "10px" }} />
                <Line type="monotone" dataKey="ndvi_smoothed" name="NDVI (SG Smoothed)" stroke="#10b981" strokeWidth={2.5} dot={false} />
                <Line type="monotone" dataKey="ndvi_raw" name="NDVI (Raw S2)" stroke="#10b981" strokeDasharray="3 3" strokeWidth={1} dot />
                <Line type="monotone" dataKey="smi_sar" name="SAR Soil Moisture (SMI)" stroke="#38bdf8" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* LST Thermal Anomaly Track */}
        <div style={{ marginTop: "16px" }}>
          <span style={{ fontSize: "12px", fontWeight: 700, color: "var(--text-main)", display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px" }}>
            <Thermometer size={14} color="#f97316" />
            Landsat-8 Thermal Baseline Anomaly (ΔT)
          </span>

          <div style={{ display: "flex", gap: "6px", overflowX: "auto", paddingBottom: "4px" }}>
            {chartData.map((d, i) => (
              <div
                key={i}
                style={{
                  flex: 1,
                  minWidth: "40px",
                  padding: "6px 2px",
                  background: "var(--bg-surface)",
                  borderRadius: "6px",
                  textAlign: "center",
                  border: d.lst_anomaly > 2.0 ? "1px solid #ef4444" : "1px solid var(--border-subtle)",
                }}
              >
                <div style={{ fontSize: "9px", color: "var(--text-dim)" }}>{d.date}</div>
                <div
                  className="telemetry-num"
                  style={{
                    fontSize: "11px",
                    fontWeight: 700,
                    marginTop: "2px",
                    color: d.lst_anomaly > 2.0 ? "#ef4444" : d.lst_anomaly > 0 ? "#f97316" : "#38bdf8",
                  }}
                >
                  {d.lst_anomaly > 0 ? `+${d.lst_anomaly}` : d.lst_anomaly}°
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <div style={{ marginTop: "24px" }}>
          <button
            onClick={() => alert(`Advisory Note for ${props.block_name} ready to export:\nRecommended Gate Discharge: ${props.recommended_discharge} m³/s\nDeficit: ${props.deficit_m3_ha} m³/ha`)}
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "6px",
              backgroundColor: "var(--accent-brand)",
              color: "#ffffff",
              border: "none",
              fontSize: "12px",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Generate Gate Discharge Directive
          </button>
        </div>
      </div>
    </div>
  );
};
