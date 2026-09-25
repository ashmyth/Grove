import React, { useState } from "react";
import {
  MapPin,
  Calendar,
  Gauge,
  Upload,
  Loader2,
  Sparkles,
} from "lucide-react";
import type { AnalysisInputPayload } from "../../types";

interface CommandControlBarProps {
  onRunAnalysis: (payload: AnalysisInputPayload) => Promise<void>;
  isRunning: boolean;
}

export const CommandControlBar: React.FC<CommandControlBarProps> = ({
  onRunAnalysis,
  isRunning,
}) => {
  const [commandArea, setCommandArea] = useState<string>("sirhind_punjab");
  const [startDate, setStartDate] = useState<string>("2026-11-01");
  const [endDate, setEndDate] = useState<string>("2026-11-08");
  const [availableDischarge, setAvailableDischarge] = useState<number>(12.5);
  const [customFileLoaded, setCustomFileLoaded] = useState<string | null>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setCustomFileLoaded(file.name);
      setCommandArea("custom_upload");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onRunAnalysis({
      command_area_id: commandArea,
      start_date: startDate,
      end_date: endDate,
      available_discharge_cumecs: availableDischarge,
    });
  };

  return (
    <div
      style={{
        backgroundColor: "var(--bg-panel)",
        borderBottom: "1px solid var(--border-subtle)",
        padding: "10px 20px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "16px",
        flexWrap: "wrap",
        zIndex: 900,
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "14px",
          flexWrap: "wrap",
          width: "100%",
          justifyContent: "space-between",
        }}
      >
        {/* Left Inputs Group */}
        <div style={{ display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
          {/* Input 1: Command Area Dropdown / Upload */}
          <div style={{ display: "flex", flexDirection: "column", gap: "3px" }}>
            <label
              style={{
                fontSize: "10px",
                fontWeight: 700,
                color: "var(--text-dim)",
                textTransform: "uppercase",
                display: "flex",
                alignItems: "center",
                gap: "4px",
              }}
            >
              <MapPin size={12} color="var(--accent-brand)" /> Command Area / ROI
            </label>
            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <select
                value={commandArea}
                onChange={(e) => setCommandArea(e.target.value)}
                style={{
                  backgroundColor: "var(--bg-surface)",
                  color: "var(--text-main)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: "6px",
                  padding: "6px 10px",
                  fontSize: "12px",
                  fontWeight: 500,
                  cursor: "pointer",
                  outline: "none",
                }}
              >
                <option value="sirhind_punjab">Sirhind Canal Command (Punjab, India)</option>
                <option value="kuttanad_kerala">Kuttanad Canal Command (Kerala, India)</option>
                <option value="bhakra_main">Bhakra Main Line (Haryana, India)</option>
                <option value="indira_gandhi">Indira Gandhi Nahar (Rajasthan, India)</option>
                <option value="tunga_bhadra">Tungabhadra Left Bank (Karnataka, India)</option>
                {customFileLoaded && (
                  <option value="custom_upload">Custom: {customFileLoaded}</option>
                )}
              </select>

              {/* Upload GeoJSON Button */}
              <label
                title="Upload Custom GeoJSON Boundary"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                  backgroundColor: "var(--bg-surface)",
                  color: "var(--text-muted)",
                  border: "1px dashed var(--border-strong)",
                  borderRadius: "6px",
                  padding: "6px 10px",
                  fontSize: "11px",
                  cursor: "pointer",
                }}
              >
                <Upload size={12} />
                <span>{customFileLoaded ? "Replace" : "Upload .geojson"}</span>
                <input
                  type="file"
                  accept=".geojson,.json,.kml"
                  onChange={handleFileUpload}
                  style={{ display: "none" }}
                />
              </label>
            </div>
          </div>

          {/* Divider */}
          <div style={{ width: "1px", height: "30px", backgroundColor: "var(--border-subtle)" }} />

          {/* Input 2: 8-Day Cycle Date Range Picker */}
          <div style={{ display: "flex", flexDirection: "column", gap: "3px" }}>
            <label
              style={{
                fontSize: "10px",
                fontWeight: 700,
                color: "var(--text-dim)",
                textTransform: "uppercase",
                display: "flex",
                alignItems: "center",
                gap: "4px",
              }}
            >
              <Calendar size={12} color="var(--accent-water)" /> 8-Day Irrigation Cycle
            </label>
            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                style={{
                  backgroundColor: "var(--bg-surface)",
                  color: "var(--text-main)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: "6px",
                  padding: "5px 8px",
                  fontSize: "12px",
                  fontFamily: "var(--font-mono)",
                  outline: "none",
                }}
              />
              <span style={{ fontSize: "11px", color: "var(--text-dim)" }}>to</span>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                style={{
                  backgroundColor: "var(--bg-surface)",
                  color: "var(--text-main)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: "6px",
                  padding: "5px 8px",
                  fontSize: "12px",
                  fontFamily: "var(--font-mono)",
                  outline: "none",
                }}
              />
            </div>
          </div>

          {/* Divider */}
          <div style={{ width: "1px", height: "30px", backgroundColor: "var(--border-subtle)" }} />

          {/* Input 3: Available Head Sluice Discharge (Q_available in cumecs) */}
          <div style={{ display: "flex", flexDirection: "column", gap: "3px", minWidth: "220px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <label
                style={{
                  fontSize: "10px",
                  fontWeight: 700,
                  color: "var(--text-dim)",
                  textTransform: "uppercase",
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                }}
              >
                <Gauge size={12} color="#f59e0b" /> Head Sluice Inflow ($Q$)
              </label>
              <span
                className="telemetry-num"
                style={{ fontSize: "12px", fontWeight: 700, color: "var(--accent-water)" }}
              >
                {availableDischarge.toFixed(1)} <span style={{ fontSize: "10px", fontWeight: 500 }}>m³/s</span>
              </span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <input
                type="range"
                min="3.0"
                max="25.0"
                step="0.5"
                value={availableDischarge}
                onChange={(e) => setAvailableDischarge(parseFloat(e.target.value))}
                style={{
                  width: "100%",
                  accentColor: "var(--accent-water)",
                  cursor: "pointer",
                }}
              />
            </div>
          </div>
        </div>

        {/* Right Action: Run Advisory Analysis Button */}
        <div>
          <button
            type="submit"
            disabled={isRunning}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              padding: "8px 18px",
              borderRadius: "6px",
              backgroundColor: isRunning ? "var(--bg-surface)" : "var(--accent-brand)",
              color: isRunning ? "var(--text-dim)" : "#ffffff",
              border: isRunning ? "1px solid var(--border-subtle)" : "none",
              fontSize: "12px",
              fontWeight: 700,
              cursor: isRunning ? "not-allowed" : "pointer",
              boxShadow: isRunning ? "none" : "0 2px 8px var(--accent-brand-glow)",
              transition: "all 0.15s ease",
            }}
          >
            {isRunning ? (
              <>
                <Loader2 size={15} style={{ animation: "spin 1s linear infinite" }} />
                <span>Computing Earth Observation...</span>
              </>
            ) : (
              <>
                <Sparkles size={15} />
                <span>Compute 8-Day Advisory</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
