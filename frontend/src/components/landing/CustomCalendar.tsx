import React, { useState, useEffect, useRef } from "react";
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon, Clock } from "lucide-react";
import "./CustomCalendar.css";

interface CustomCalendarProps {
  startDate: string; // YYYY-MM-DD
  endDate: string;   // YYYY-MM-DD
  onChange: (start: string, end: string) => void;
  onClose: () => void;
  activePill?: "start" | "end";
}

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const WEEKDAYS = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"];

export const CustomCalendar: React.FC<CustomCalendarProps> = ({
  startDate,
  endDate,
  onChange,
  onClose,
  activePill = "start",
}) => {
  const popoverRef = useRef<HTMLDivElement>(null);

  // Parse initial dates
  const initialDate = startDate ? new Date(startDate) : new Date(2026, 10, 1);
  const [currentYear, setCurrentYear] = useState<number>(initialDate.getFullYear() || 2026);
  const [currentMonth, setCurrentMonth] = useState<number>(initialDate.getMonth() || 10); // 0-indexed (10 = Nov)

  const [tempStart, setTempStart] = useState<string>(startDate || "2026-11-01");
  const [tempEnd, setTempEnd] = useState<string>(endDate || "2026-11-08");
  const [selectionStep, setSelectionStep] = useState<"picking_start" | "picking_end">(
    activePill === "end" ? "picking_end" : "picking_start"
  );

  // Close on outside click
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        onClose();
      }
    };
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    document.addEventListener("mousedown", handleOutsideClick);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [onClose]);

  // Navigate months
  const handlePrevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear((y) => y - 1);
    } else {
      setCurrentMonth((m) => m - 1);
    }
  };

  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear((y) => y + 1);
    } else {
      setCurrentMonth((m) => m + 1);
    }
  };

  // Calendar matrix calculation
  const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const daysInPrevMonth = new Date(currentYear, currentMonth, 0).getDate();

  const formatDateStr = (y: number, m: number, d: number) => {
    const mm = String(m + 1).padStart(2, "0");
    const dd = String(d).padStart(2, "0");
    return `${y}-${mm}-${dd}`;
  };

  // Handle day click
  const handleDayClick = (dayStr: string) => {
    if (selectionStep === "picking_start") {
      setTempStart(dayStr);
      // Auto-set end to 8 days later by default or prompt end
      const d = new Date(dayStr);
      d.setDate(d.getDate() + 7);
      const autoEnd = formatDateStr(d.getFullYear(), d.getMonth(), d.getDate());
      setTempEnd(autoEnd);
      setSelectionStep("picking_end");
    } else {
      // picking_end
      if (new Date(dayStr) < new Date(tempStart)) {
        setTempStart(dayStr);
      } else {
        setTempEnd(dayStr);
        setSelectionStep("picking_start");
      }
    }
  };

  // Preset rotation durations
  const applyPresetDays = (days: number) => {
    const start = new Date(tempStart);
    const end = new Date(start);
    end.setDate(start.getDate() + (days - 1));
    const endStr = formatDateStr(end.getFullYear(), end.getMonth(), end.getDate());
    setTempEnd(endStr);
  };

  const handleApply = () => {
    onChange(tempStart, tempEnd);
    onClose();
  };

  // Range checks
  const isStart = (dStr: string) => dStr === tempStart;
  const isEnd = (dStr: string) => dStr === tempEnd;
  const isInRange = (dStr: string) => {
    if (!tempStart || !tempEnd) return false;
    return dStr > tempStart && dStr < tempEnd;
  };

  // Compute days count
  const sDate = new Date(tempStart);
  const eDate = new Date(tempEnd);
  const diffDays = Math.max(1, Math.round((eDate.getTime() - sDate.getTime()) / (1000 * 3600 * 24)) + 1);

  return (
    <div className="calendar-window-overlay" onClick={onClose}>
      <div
        className="calendar-window-box"
        ref={popoverRef}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        {/* Window Title Bar */}
        <div className="calendar-window-titlebar">
          <div className="window-dots">
            <span className="dot red" onClick={onClose} title="Close window" />
            <span className="dot yellow" />
            <span className="dot green" />
          </div>
          <div className="calendar-header-title">
            <CalendarIcon size={14} className="calendar-title-icon" />
            <span>IRRIGATION CYCLE WINDOW</span>
          </div>
          <button type="button" className="calendar-close-x" onClick={onClose} title="Close window">
            ×
          </button>
        </div>

      {/* Preset Rotation Pills */}
      <div className="calendar-preset-bar">
        <button
          type="button"
          className={`calendar-preset-chip ${diffDays === 8 ? "active" : ""}`}
          onClick={() => applyPresetDays(8)}
        >
          8-Day Satellite Rotation
        </button>
        <button
          type="button"
          className={`calendar-preset-chip ${diffDays === 14 ? "active" : ""}`}
          onClick={() => applyPresetDays(14)}
        >
          14-Day Biweekly
        </button>
        <button
          type="button"
          className={`calendar-preset-chip ${diffDays === 30 ? "active" : ""}`}
          onClick={() => applyPresetDays(30)}
        >
          30-Day Canal Period
        </button>
      </div>

      {/* Month Navigator */}
      <div className="calendar-month-nav">
        <button type="button" className="nav-arrow-btn" onClick={handlePrevMonth} title="Previous Month">
          <ChevronLeft size={16} />
        </button>
        <span className="current-month-label">
          {MONTH_NAMES[currentMonth].toUpperCase()} {currentYear}
        </span>
        <button type="button" className="nav-arrow-btn" onClick={handleNextMonth} title="Next Month">
          <ChevronRight size={16} />
        </button>
      </div>

      {/* Weekdays Row */}
      <div className="calendar-weekdays-grid">
        {WEEKDAYS.map((wd) => (
          <span key={wd} className="weekday-col">
            {wd}
          </span>
        ))}
      </div>

      {/* Days Matrix */}
      <div className="calendar-days-grid">
        {/* Leading overflow days from prev month */}
        {Array.from({ length: firstDayOfMonth }).map((_, i) => {
          const dayNum = daysInPrevMonth - firstDayOfMonth + i + 1;
          return (
            <div key={`prev-${i}`} className="calendar-day-cell overflow-day">
              {dayNum}
            </div>
          );
        })}

        {/* Days of current month */}
        {Array.from({ length: daysInMonth }).map((_, i) => {
          const dayNum = i + 1;
          const dayStr = formatDateStr(currentYear, currentMonth, dayNum);
          const startCell = isStart(dayStr);
          const endCell = isEnd(dayStr);
          const rangeCell = isInRange(dayStr);

          return (
            <button
              key={dayStr}
              type="button"
              className={`calendar-day-cell current-month-day ${
                startCell ? "is-start" : ""
              } ${endCell ? "is-end" : ""} ${rangeCell ? "is-in-range" : ""}`}
              onClick={() => handleDayClick(dayStr)}
            >
              {dayNum}
            </button>
          );
        })}

        {/* Trailing overflow days */}
        {Array.from({ length: (7 - ((firstDayOfMonth + daysInMonth) % 7)) % 7 }).map((_, i) => (
          <div key={`next-${i}`} className="calendar-day-cell overflow-day">
            {i + 1}
          </div>
        ))}
      </div>

      {/* Footer Info & Apply */}
      <div className="calendar-popover-footer">
        <div className="range-preview-badge">
          <Clock size={12} />
          <span>
            {tempStart} → {tempEnd} ({diffDays} Days)
          </span>
        </div>
        <div className="calendar-footer-actions">
          <button type="button" className="calendar-cancel-btn" onClick={onClose}>
            Cancel
          </button>
          <button type="button" className="calendar-apply-btn" onClick={handleApply}>
            Apply Period
          </button>
        </div>
      </div>
    </div>
  );
};
