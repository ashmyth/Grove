import React, { useState, useRef } from "react";
import { Plus, Minus, Info, MapPin, Check, ArrowRight } from "lucide-react";
import type { AnalysisInputPayload } from "../../types";
import "./LandingConsole.css";

interface LandingConsoleProps {
  onLaunch: (payload: AnalysisInputPayload) => void;
  isLoading?: boolean;
}

const PRESET_AREAS = [
  { id: "sirhind_punjab", name: "Sirhind Canal Command, Punjab", state: "Punjab, India", baseline: 12.5 },
  { id: "kuttanad_kerala", name: "Kuttanad Canal System, Kerala", state: "Kerala, India", baseline: 8.0 },
  { id: "tunga_bhadra", name: "Tungabhadra Left Bank, Karnataka", state: "Karnataka / AP, India", baseline: 29.5 },
  { id: "bhakra_main", name: "Bhakra Main Line, Haryana", state: "Haryana, India", baseline: 22.0 },
  { id: "indira_gandhi", name: "Indira Gandhi Canal, Rajasthan", state: "Rajasthan, India", baseline: 35.0 },
];

export const LandingConsole: React.FC<LandingConsoleProps> = ({ onLaunch, isLoading = false }) => {
  const [selectedAreaId, setSelectedAreaId] = useState<string>("sirhind_punjab");
  const [areaInputText, setAreaInputText] = useState<string>("Sirhind Canal Command, Punjab");
  const [startDate, setStartDate] = useState<string>("2026-11-01");
  const [endDate, setEndDate] = useState<string>("2026-11-08");
  const [discharge, setDischarge] = useState<number>(29.5);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [customGeoJSON, setCustomGeoJSON] = useState<any>(null);
  const [isAreaDropdownOpen, setIsAreaDropdownOpen] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle multi-file GeoJSON upload and auto-merge
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const fileList = Array.from(files);
    setUploadedFiles(fileList);

    // Read and merge all GeoJSON files
    const mergedFeatures: any[] = [];
    for (const file of fileList) {
      try {
        const text = await file.text();
        const json = JSON.parse(text);
        if (json.type === "FeatureCollection" && Array.isArray(json.features)) {
          mergedFeatures.push(...json.features);
        } else if (json.type === "Feature") {
          mergedFeatures.push(json);
        }
      } catch (err) {
        console.error(`Error reading ${file.name}:`, err);
      }
    }

    if (mergedFeatures.length > 0) {
      const unifiedCollection = {
        type: "FeatureCollection",
        features: mergedFeatures,
      };
      setCustomGeoJSON(unifiedCollection);
      setAreaInputText(`Custom: ${fileList.length} GeoJSON${fileList.length > 1 ? "s" : ""} (${mergedFeatures.length} parcels)`);
      setSelectedAreaId("custom_upload");
    }
  };

  const handleSelectPreset = (preset: typeof PRESET_AREAS[0]) => {
    setSelectedAreaId(preset.id);
    setAreaInputText(preset.name);
    setDischarge(preset.baseline);
    setIsAreaDropdownOpen(false);
  };

  const handleLaunch = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    onLaunch({
      command_area_id: selectedAreaId,
      start_date: startDate,
      end_date: endDate,
      available_discharge_cumecs: discharge,
      custom_geojson: customGeoJSON,
    });
  };

  return (
    <div className="grove-landing-wrapper">
      {/* Background Ambient Glow */}
      <div className="landing-ambient-glow" />

      {/* Main Container */}
      <div className="grove-landing-content">
        {/* Brand Logo Header */}
        <div className="grove-brand-header">
          <div className="grove-logo-mark">
            <span className="logo-letter letter-g">g</span>
            <span className="logo-letter letter-r">r</span>
            <span className="logo-letter letter-o">o</span>
            <span className="logo-letter letter-v">v</span>
            <span className="logo-letter letter-e">e</span>
          </div>
          <p className="grove-subheading">AI-Driven Automated Crop Mapping & 8-Day Canal Command Advisory</p>
        </div>

        {/* Central Floating Console Card */}
        <div className="grove-console-card">
          {/* Top Section: Area Selector (White) */}
          <div className="console-top-section">
            <div className="area-input-container">
              <input
                type="text"
                className="area-text-input"
                value={areaInputText}
                onChange={(e) => {
                  setAreaInputText(e.target.value);
                  setIsAreaDropdownOpen(true);
                }}
                onFocus={() => setIsAreaDropdownOpen(true)}
                placeholder="Search or type canal command area..."
              />
              <div className="area-underline" />

              {/* Autocomplete Dropdown */}
              {isAreaDropdownOpen && (
                <div className="area-dropdown-menu">
                  {PRESET_AREAS.map((p) => (
                    <div
                      key={p.id}
                      className="area-dropdown-item"
                      onClick={() => handleSelectPreset(p)}
                    >
                      <MapPin size={14} className="dropdown-pin-icon" />
                      <div className="dropdown-item-details">
                        <span className="item-name">{p.name}</span>
                        <span className="item-state">{p.state}</span>
                      </div>
                    </div>
                  ))}
                  <div
                    className="area-dropdown-close"
                    onClick={() => setIsAreaDropdownOpen(false)}
                  >
                    Close
                  </div>
                </div>
              )}
            </div>

            {/* Right Side: Area Outline Icon Badge */}
            <div className="area-badge">
              <svg
                width="28"
                height="22"
                viewBox="0 0 28 22"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="area-polygon-svg"
              >
                <path
                  d="M2 13L6 4L14 2L22 6L26 12L21 19L9 20L2 13Z"
                  stroke="#111111"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
              </svg>
              <span className="area-badge-label">Area</span>
            </div>
          </div>

          {/* Bottom Section: Controls (Black) */}
          <div className="console-bottom-section">
            {/* Box 1: Multi-file GeoJSON Upload Tile */}
            <div
              className={`upload-geojson-box ${uploadedFiles.length > 0 ? "has-files" : ""}`}
              onClick={() => fileInputRef.current?.click()}
              title="Click to select single or multiple .geojson files"
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".geojson,.json,.kml"
                onChange={handleFileUpload}
                style={{ display: "none" }}
              />
              {uploadedFiles.length > 0 ? (
                <div className="upload-active-state">
                  <Check size={22} className="upload-check-icon" />
                  <span className="upload-title">
                    {uploadedFiles.length} File{uploadedFiles.length > 1 ? "s" : ""}
                  </span>
                  <span className="upload-subtitle">GeoJSON Loaded</span>
                </div>
              ) : (
                <div className="upload-empty-state">
                  <Plus size={26} strokeWidth={1.5} className="upload-plus-icon" />
                  <span className="upload-label">Upload Geojson</span>
                </div>
              )}
            </div>

            {/* Box 2: Visual Indicator Thumbnail */}
            <div className="console-indicator-tile">
              <div className="indicator-gradient-glow" />
              <div className="indicator-inner-content">
                <span className="indicator-tag">ACTIVE PILOT</span>
                <span className="indicator-pilot-name">
                  {selectedAreaId === "sirhind_punjab"
                    ? "Sirhind (Alluvial)"
                    : selectedAreaId === "kuttanad_kerala"
                    ? "Kuttanad (Wetland)"
                    : "Command Area"}
                </span>
                <span className="indicator-sat-badge">10m Sentinel-1/2</span>
              </div>
            </div>

            {/* Box 3: Timeline Date Range */}
            <div className="console-timeline-section">
              <div className="timeline-header">
                <span className="timeline-title">Timeline</span>
                <span className="timeline-subtitle">Choose the irrigation cycle time period</span>
              </div>
              <div className="timeline-inputs-row">
                <div className="date-pill-wrapper">
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="date-pill-input"
                  />
                </div>
                <span className="timeline-arrow">to</span>
                <div className="date-pill-wrapper">
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="date-pill-input"
                  />
                </div>
              </div>
            </div>

            {/* Box 4: Discharge Stepper (Q in Cumecs) */}
            <div className="console-stepper-section">
              <div className="stepper-info-icon" title="Target head canal available discharge in cumecs (m³/s)">
                <Info size={11} />
              </div>
              <button
                type="button"
                className="stepper-btn btn-plus"
                onClick={() => setDischarge((prev) => Math.min(50, +(prev + 1.0).toFixed(1)))}
              >
                <Plus size={14} />
              </button>
              <div className="stepper-value-container">
                <span className="stepper-number">{discharge.toFixed(1)}</span>
                <span className="stepper-unit">cumecs</span>
              </div>
              <button
                type="button"
                className="stepper-btn btn-minus"
                onClick={() => setDischarge((prev) => Math.max(2.0, +(prev - 1.0).toFixed(1)))}
              >
                <Minus size={14} />
              </button>
            </div>
          </div>
        </div>

        {/* Action Trigger Button */}
        <div className="console-action-footer">
          <button
            type="button"
            className="grove-launch-button"
            onClick={() => handleLaunch()}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="launch-spinner" />
                <span>INITIALIZING SATELLITE ENGINE...</span>
              </>
            ) : (
              <>
                <span>INITIALIZE COMMAND DECK</span>
                <ArrowRight size={18} className="launch-arrow-icon" />
              </>
            )}
          </button>
          <div className="console-meta-info">
            <span>Harmonized Landsat-Sentinel • IBM-NASA Prithvi-EO 100M • FAO-56 Hydrology</span>
          </div>
        </div>
      </div>
    </div>
  );
};
