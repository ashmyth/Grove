import React from "react";
import { Moon, Sun, Download, RefreshCw, Satellite, Radio } from "lucide-react";

interface HeaderProps {
  theme: "dark" | "light";
  onToggleTheme: () => void;
  onRefresh: () => void;
  onExport: () => void;
  cycleDays: number;
}

export const Header: React.FC<HeaderProps> = ({
  theme,
  onToggleTheme,
  onRefresh,
  onExport,
  cycleDays,
}) => {
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 20px",
        height: "56px",
        backgroundColor: "var(--bg-panel)",
        borderBottom: "1px solid var(--border-subtle)",
        zIndex: 1000,
        position: "relative",
      }}
    >
      {/* Brand Identity */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "32px",
            height: "32px",
            borderRadius: "8px",
            background: "var(--accent-brand-glow)",
            border: "1px solid var(--accent-brand)",
            color: "var(--accent-brand)",
          }}
        >
          <Satellite size={18} />
        </div>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ fontWeight: 700, fontSize: "16px", letterSpacing: "-0.01em" }}>
              GROVE
            </span>
            <span
              style={{
                fontSize: "11px",
                fontWeight: 600,
                padding: "1px 6px",
                borderRadius: "4px",
                backgroundColor: "var(--bg-surface)",
                color: "var(--text-dim)",
                border: "1px solid var(--border-subtle)",
              }}
            >
              GEOPRITHVI-AGRI
            </span>
          </div>
          <span style={{ fontSize: "11px", color: "var(--text-dim)", display: "block" }}>
            Multimodal Remote Sensing & Canal Command Water Deficit Engine
          </span>
        </div>
      </div>

      {/* Center Status Banner */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          backgroundColor: "var(--bg-surface)",
          padding: "6px 14px",
          borderRadius: "20px",
          border: "1px solid var(--border-subtle)",
        }}
      >
        <Radio size={14} color="var(--accent-brand)" style={{ animation: "pulse 2s infinite" }} />
        <span style={{ fontSize: "12px", color: "var(--text-muted)" }}>
          Active Cycle: <strong className="telemetry-num">{cycleDays}-Day</strong> Canal Rotation
        </span>
        <span style={{ width: "4px", height: "4px", borderRadius: "50%", background: "var(--border-strong)" }} />
        <span style={{ fontSize: "11px", color: "var(--accent-brand)", fontWeight: 600 }}>
          S1 SAR + S2 Optical Synchronized
        </span>
      </div>

      {/* Action Controls */}
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <button
          onClick={onRefresh}
          title="Refresh Data"
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            padding: "6px 12px",
            borderRadius: "6px",
            backgroundColor: "var(--bg-surface)",
            color: "var(--text-main)",
            border: "1px solid var(--border-subtle)",
            fontSize: "12px",
            cursor: "pointer",
          }}
        >
          <RefreshCw size={14} />
          <span>Sync</span>
        </button>

        <button
          onClick={onExport}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            padding: "6px 14px",
            borderRadius: "6px",
            backgroundColor: "var(--accent-water)",
            color: "#ffffff",
            border: "none",
            fontSize: "12px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          <Download size={14} />
          <span>Export Advisory</span>
        </button>

        <button
          onClick={onToggleTheme}
          title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "32px",
            height: "32px",
            borderRadius: "6px",
            backgroundColor: "var(--bg-surface)",
            color: "var(--text-main)",
            border: "1px solid var(--border-subtle)",
            cursor: "pointer",
          }}
        >
          {theme === "dark" ? <Sun size={15} /> : <Moon size={15} />}
        </button>
      </div>
    </header>
  );
};
