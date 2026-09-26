import React, { useState, useRef } from "react";
import { Plus, Minus, Info, MapPin, Check, ArrowRight, Clock } from "lucide-react";
import type { AnalysisInputPayload } from "../../types";
import groveLogo from "../../assets/grove-logo.svg";
import { CustomCalendar } from "./CustomCalendar";
import "./LandingConsole.css";

interface LandingConsoleProps {
  onLaunch: (payload: AnalysisInputPayload) => void;
  isLoading?: boolean;
}

const PRESET_AREAS = [
  { id: "sirhind_punjab", name: "Sirhind Canal Command, Punjab", state: "Punjab, India", baseline: 29.5 },
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
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [activeCalendarPill, setActiveCalendarPill] = useState<"start" | "end">("start");

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Helper to display dates strictly in dd-mm-yyyy format matching Paper design
  const formatToDMY = (isoDate: string) => {
    if (!isoDate) return "dd-mm-yyyy";
    const parts = isoDate.split("-");
    if (parts.length === 3) {
      return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }
    return isoDate;
  };

  // Handle multi-file GeoJSON upload and auto-merge
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const fileList = Array.from(files);
    setUploadedFiles(fileList);

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
      {/* Main Container */}
      <div className="grove-landing-content">
        {/* Brand Logo Header */}
        <div className="grove-brand-header">
          <img src={groveLogo} alt="Grove" className="grove-brand-logo-img" />
        </div>

        {/* Central Floating Console Card Matching Paper LX-0 */}
        <div className="grove-console-card">
          {/* Top Section: Area Selector (White #FFFFFF) */}
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
                placeholder="Search canal command area..."
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

            {/* Right Side: Area Outline Polygon Icon + Label (Exact Paper SVG) */}
            <div className="area-badge" onClick={() => setIsAreaDropdownOpen(!isAreaDropdownOpen)}>
              <svg
                width="23"
                height="20"
                viewBox="0 0 23 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="area-polygon-svg"
              >
                <path
                  d="M1.410 6.190C1.934 5.673 3.238 4.300 4.122 2.889C4.352 2.522 4.342 2.130 4.538 1.850C4.788 1.492 5.435 1.696 5.850 1.804C6.637 2.008 7.056 2.559 7.339 2.754C7.897 3.136 8.630 2.304 9.330 1.935C10.181 1.487 10.994 2.428 11.585 2.883C12.328 3.455 13.574 2.690 14.409 2.927C14.590 2.978 14.758 3.035 14.934 3.057C15.110 3.079 15.284 3.079 15.460 2.887C16.339 1.924 16.424 1.052 16.927 0.402C17.166 0.094 17.605 0.055 17.977 0.011C18.800 -0.085 19.486 0.442 20.231 0.981C20.680 1.306 21.108 1.522 21.348 1.845C22.105 2.861 21.461 4.458 20.980 6.635C20.877 7.103 20.718 7.225 20.673 7.376C20.580 7.686 20.889 7.918 21.151 8.304C22.299 9.989 20.673 11.458 20.323 12.258C20.235 12.454 20.148 12.625 20.017 12.756C19.885 12.887 19.712 12.972 19.533 13.060M1.278 6.320C1.105 6.320 0.799 6.363 0.406 6.577C-0.091 6.848 -0.035 7.742 0.073 8.432C0.247 9.537 0.753 10.333 0.622 11.113C0.564 11.464 0.447 11.848 0.425 12.279C0.413 12.497 0.532 12.710 0.685 12.863C0.838 13.016 1.055 13.102 1.253 13.103C2.018 13.108 2.458 11.985 3.201 10.969C4.119 9.715 4.823 9.389 5.107 9.194C5.389 9.000 5.742 9.559 5.961 9.839C6.397 10.397 6.182 11.456 5.876 12.280C5.809 12.462 5.702 12.625 5.722 12.777C5.742 12.930 5.872 13.058 6.048 13.103C6.904 13.321 7.841 12.801 8.432 12.694C9.196 12.556 9.026 11.506 9.396 11.312C10.383 10.794 11.082 11.505 11.476 11.590C11.868 11.676 12.046 12.237 12.222 12.647C12.301 12.832 12.224 13.014 12.115 13.145C11.625 13.733 10.695 14.180 9.818 14.722C9.412 14.973 8.985 15.133 8.679 15.413C8.390 15.677 8.327 16.083 8.261 16.428C8.228 16.600 8.239 16.773 8.694 16.861C10.036 17.121 11.170 16.906 11.541 16.949C12.633 17.073 12.833 18.588 13.402 19.151C13.735 19.480 14.191 19.713 14.540 19.951C14.695 20.056 14.890 19.975 15.044 19.867C15.706 19.405 15.985 18.551 16.816 18.052C17.715 17.512 18.480 18.502 20.772 18.549C21.504 18.564 21.765 17.988 22.027 17.665C22.652 16.895 22.554 16.003 22.903 15.267C22.986 15.091 23.035 14.922 22.970 14.748C22.656 13.899 21.769 13.452 21.330 12.868C21.025 12.716 20.630 12.672 20.215 12.714C20.017 12.757 19.843 12.843 19.533 12.931"
                  stroke="#000000"
                  strokeWidth="1.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <span className="area-badge-label">Area</span>
            </div>
          </div>

          {/* Bottom Section: Controls (Black #000000) */}
          <div className="console-bottom-section">
            {/* Box 1: Multi-file GeoJSON Upload Tile (198px x 140px, Dashed White) */}
            <div
              className="upload-geojson-box"
              onClick={() => fileInputRef.current?.click()}
              title="Click to upload .geojson file"
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".geojson,.json,.kml"
                onChange={handleFileUpload}
                style={{ display: "none" }}
              />
              <div className="upload-empty-state">
                <svg
                  viewBox="0 0 45 43"
                  width="45"
                  height="43"
                  xmlns="http://www.w3.org/2000/svg"
                  className="upload-plus-svg"
                >
                  <path
                    d="M23.523 0V43M45 22.477H0"
                    stroke="#FFFFFF"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                  />
                </svg>
                <span className="upload-label">Upload Geojson</span>
              </div>
            </div>

            {/* Box 2: Uploaded GeoJSON Card (Fades into darkness) - ONLY rendered when a GeoJSON is added! */}
            {uploadedFiles.length > 0 && (
              <div
                className="uploaded-fade-card"
                title={`${uploadedFiles.length} file(s) loaded. Click to add more or clear.`}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="uploaded-card-info">
                  <span className="uploaded-tag">GEOJSON LOADED</span>
                  <span className="uploaded-name">
                    {uploadedFiles[0]?.name || "custom.geojson"}
                  </span>
                  <span className="uploaded-meta">
                    {customGeoJSON?.features?.length || 1} parcel{customGeoJSON?.features?.length === 1 ? "" : "s"}
                  </span>
                </div>
                <button
                  type="button"
                  className="uploaded-clear-btn"
                  title="Remove uploaded GeoJSON"
                  onClick={(e) => {
                    e.stopPropagation();
                    setUploadedFiles([]);
                    setCustomGeoJSON(null);
                    setAreaInputText("Sirhind Canal Command, Punjab");
                    setSelectedAreaId("sirhind_punjab");
                    if (fileInputRef.current) fileInputRef.current.value = "";
                  }}
                >
                  ×
                </button>
              </div>
            )}

            {/* Box 3: Timeline Section (Enlarged Capsule with Center Arrow & Clock Icon) */}
            <div className="console-timeline-section">
              <div className="timeline-header">
                <div className="timeline-title-group">
                  <Clock size={20} className="timeline-clock-icon" strokeWidth={2} />
                  <span className="timeline-title">Timeline</span>
                </div>
                <div className="timeline-subtitle">
                  Choose the irrigation cycle<br />time period
                </div>
              </div>

              {/* Enlarged White Capsule Bar with Center Arrow */}
              <div className="timeline-capsule-bar">
                <button
                  type="button"
                  className={`date-capsule-item ${isCalendarOpen && activeCalendarPill === "start" ? "is-active-pill" : ""}`}
                  onClick={() => {
                    setActiveCalendarPill("start");
                    setIsCalendarOpen(true);
                  }}
                  title="Click to select start date via custom calendar"
                >
                  <span className="date-pill-text">
                    {startDate ? formatToDMY(startDate) : "dd-mm-yyyy"}
                  </span>
                </button>

                {/* Center Arrow */}
                <div className="timeline-capsule-arrow" aria-hidden="true">
                  <svg width="24" height="16" viewBox="0 0 24 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M2 8H20M20 8L13 1.5M20 8L13 14.5"
                      stroke="#000000"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>

                <button
                  type="button"
                  className={`date-capsule-item ${isCalendarOpen && activeCalendarPill === "end" ? "is-active-pill" : ""}`}
                  onClick={() => {
                    setActiveCalendarPill("end");
                    setIsCalendarOpen(true);
                  }}
                  title="Click to select end date via custom calendar"
                >
                  <span className="date-pill-text">
                    {endDate ? formatToDMY(endDate) : "dd-mm-yyyy"}
                  </span>
                </button>
              </div>

              {/* Custom Calendar Popover anchored above capsule */}
              {isCalendarOpen && (
                <CustomCalendar
                  startDate={startDate}
                  endDate={endDate}
                  activePill={activeCalendarPill}
                  onChange={(newStart, newEnd) => {
                    setStartDate(newStart);
                    setEndDate(newEnd);
                  }}
                  onClose={() => setIsCalendarOpen(false)}
                />
              )}
            </div>

            {/* Box 4: Sluice Discharge Stepper (Enlarged 46px Rounded Buttons & m3/s) */}
            <div className="console-stepper-section">
              <div className="stepper-info-icon" title="Target canal available discharge in cumecs (m³/s)">
                <Info size={11} stroke="#FFFFFF" />
              </div>
              <button
                type="button"
                className="stepper-btn btn-plus"
                onClick={() => setDischarge((prev) => Math.min(50, +(prev + 1.0).toFixed(1)))}
                title="Increase discharge"
              >
                <Plus size={19} stroke="#FFFFFF" strokeWidth={2.2} />
              </button>
              <div className="stepper-value-container">
                <span className="stepper-number">{discharge.toFixed(1)}</span>
                <span className="stepper-unit">m3/s</span>
              </div>
              <button
                type="button"
                className="stepper-btn btn-minus"
                onClick={() => setDischarge((prev) => Math.max(2.0, +(prev - 1.0).toFixed(1)))}
                title="Decrease discharge"
              >
                <Minus size={19} stroke="#000000" strokeWidth={2.4} />
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
