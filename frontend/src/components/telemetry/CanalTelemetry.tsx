import React from "react";
import type { CanalAdvisoryItem, CommandOverview, ReachType } from "../../types";
import { AlertTriangle, Droplets, Gauge, MapPin } from "lucide-react";

interface CanalTelemetryProps {
  overview: CommandOverview | null;
  advisories: CanalAdvisoryItem[];
  selectedParcelId: string | null;
  onSelectParcel: (id: string) => void;
  reachFilter: ReachType | "all";
  onFilterReach: (reach: ReachType | "all") => void;
}

export const CanalTelemetry: React.FC<CanalTelemetryProps> = ({
  overview,
  advisories,
  selectedParcelId,
  onSelectParcel,
  reachFilter,
  onFilterReach,
}) => {
  return (
    <aside
      style={{
        width: "350px",
        minWidth: "350px",
        height: "calc(100vh - 56px)",
        backgroundColor: "var(--bg-panel)",
        borderRight: "1px solid var(--border-subtle)",
        display: "flex",
        flexDirection: "column",
        overflowY: "auto",
        zIndex: 500,
      }}
    >
      {/* Top Telemetry KPI Bar */}
      <div style={{ padding: "16px", borderBottom: "1px solid var(--border-subtle)" }}>
        <span
          style={{
            fontSize: "11px",
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            color: "var(--text-dim)",
            display: "block",
            marginBottom: "12px",
          }}
        >
          Canal Command Telemetry
        </span>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
          {/* Discharge Allocation */}
          <div
            style={{
              padding: "10px",
              borderRadius: "8px",
              backgroundColor: "var(--bg-surface)",
              border: "1px solid var(--border-subtle)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "var(--accent-water)", marginBottom: "4px" }}>
              <Gauge size={14} />
              <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>Target Discharge</span>
            </div>
            <div className="telemetry-num" style={{ fontSize: "18px", fontWeight: 700 }}>
              {overview?.total_recommended_discharge_cumecs || "0.00"}{" "}
              <span style={{ fontSize: "11px", fontWeight: 500, color: "var(--text-dim)" }}>m³/s</span>
            </div>
          </div>

          {/* Water Deficit */}
          <div
            style={{
              padding: "10px",
              borderRadius: "8px",
              backgroundColor: "var(--bg-surface)",
              border: "1px solid var(--border-subtle)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "var(--stress-severe)", marginBottom: "4px" }}>
              <Droplets size={14} />
              <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>Total Deficit</span>
            </div>
            <div className="telemetry-num" style={{ fontSize: "18px", fontWeight: 700 }}>
              {overview ? (overview.total_deficit_m3 / 1000).toFixed(1) : "0.0"}{" "}
              <span style={{ fontSize: "11px", fontWeight: 500, color: "var(--text-dim)" }}>k m³</span>
            </div>
          </div>
        </div>

        {/* Severe Alert Strip */}
        {overview && overview.severe_stress_parcels_count > 0 && (
          <div
            style={{
              marginTop: "10px",
              padding: "8px 12px",
              borderRadius: "6px",
              backgroundColor: "oklch(0.60 0.22 25 / 0.12)",
              border: "1px solid oklch(0.60 0.22 25 / 0.3)",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <AlertTriangle size={15} color="var(--stress-severe)" />
            <span style={{ fontSize: "11px", color: "var(--stress-severe)", fontWeight: 600 }}>
              {overview.severe_stress_parcels_count} Tail-End Parcels in Severe Water Deficit
            </span>
          </div>
        )}
      </div>

      {/* Reach Filtering Tabs */}
      <div
        style={{
          display: "flex",
          padding: "10px 16px",
          gap: "6px",
          borderBottom: "1px solid var(--border-subtle)",
          backgroundColor: "var(--bg-panel)",
        }}
      >
        {(["all", "head", "middle", "tail"] as const).map((r) => (
          <button
            key={r}
            onClick={() => onFilterReach(r)}
            style={{
              flex: 1,
              padding: "5px 0",
              fontSize: "11px",
              fontWeight: 600,
              textTransform: "capitalize",
              borderRadius: "5px",
              border: reachFilter === r ? "1px solid var(--accent-brand)" : "1px solid var(--border-subtle)",
              backgroundColor: reachFilter === r ? "var(--accent-brand-glow)" : "var(--bg-surface)",
              color: reachFilter === r ? "var(--accent-brand)" : "var(--text-muted)",
              cursor: "pointer",
            }}
          >
            {r}
          </button>
        ))}
      </div>

      {/* Priority Canal Advisory List */}
      <div style={{ flex: 1, overflowY: "auto", padding: "12px 16px" }}>
        <span
          style={{
            fontSize: "11px",
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            color: "var(--text-dim)",
            display: "block",
            marginBottom: "10px",
          }}
        >
          Canal Distributary Advisories ({advisories.length})
        </span>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {advisories.map((item) => {
            const isSelected = selectedParcelId === item.id;
            const badgeClass =
              item.stress_level === "Severe"
                ? "badge-severe"
                : item.stress_level === "Moderate"
                ? "badge-moderate"
                : item.stress_level === "Mild"
                ? "badge-mild"
                : "badge-normal";

            return (
              <div
                key={item.id}
                onClick={() => onSelectParcel(item.id)}
                style={{
                  padding: "12px",
                  borderRadius: "8px",
                  backgroundColor: isSelected ? "var(--bg-surface-hover)" : "var(--bg-surface)",
                  border: isSelected ? "1px solid var(--accent-brand)" : "1px solid var(--border-subtle)",
                  cursor: "pointer",
                  transition: "all 0.15s ease",
                }}
              >
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "6px" }}>
                  <div>
                    <span style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-main)", display: "block" }}>
                      {item.block_name}
                    </span>
                    <span style={{ fontSize: "11px", color: "var(--text-dim)", display: "flex", alignItems: "center", gap: "3px" }}>
                      <MapPin size={10} /> {item.id} • {item.crop_type} ({item.stage})
                    </span>
                  </div>
                  <span
                    className={badgeClass}
                    style={{
                      fontSize: "10px",
                      fontWeight: 700,
                      padding: "2px 6px",
                      borderRadius: "4px",
                      textTransform: "uppercase",
                    }}
                  >
                    {item.stress_level}
                  </span>
                </div>

                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    paddingTop: "6px",
                    borderTop: "1px dashed var(--border-subtle)",
                    fontSize: "11px",
                  }}
                >
                  <span style={{ color: "var(--text-muted)" }}>
                    Deficit: <strong className="telemetry-num">{item.deficit_m3_ha}</strong> m³/ha
                  </span>
                  <span style={{ color: "var(--accent-water)" }}>
                    Alloc: <strong className="telemetry-num">{item.discharge_cumecs}</strong> cumecs
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </aside>
  );
};
