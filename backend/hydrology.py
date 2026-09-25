"""
Grove (GeoPrithvi-Agri) - Satellite Hydrology & Irrigation Deficit Engine
Implements Interface Contract 2 & PyET standard formulations:
- Hargreaves-Samani Reference Evapotranspiration (ETo)
- Dynamic FAO-56 stage-dependent crop coefficients (Kc)
- USDA SCS Effective Rainfall (Peff)
- 8-Day Volumetric Crop Water Deficit & Sluice Gate Hydraulics (Q = V / t)
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

try:
    import pyet
    _PYET_AVAILABLE = True
except ImportError:
    _PYET_AVAILABLE = False

# FAO-56 Crop Coefficients Table (Kc) across Phenological Growth Stages
# Stage 1: Initial / Vegetative (CRI / Emergence)
# Stage 2: Mid-Season (Tillering, Peak Flowering, Booting, Boll Formation)
# Stage 3: Late-Season (Grain Filling, Ripening, Senescence)
FAO56_KC_TABLE = {
    "paddy": {"initial": 1.05, "mid": 1.20, "late": 0.90},
    "rice": {"initial": 1.05, "mid": 1.20, "late": 0.90},
    "wheat": {"initial": 0.35, "mid": 1.15, "late": 0.25},
    "cotton": {"initial": 0.35, "mid": 1.20, "late": 0.60},
    "sugarcane": {"initial": 0.40, "mid": 1.25, "late": 0.75},
    "maize": {"initial": 0.30, "mid": 1.20, "late": 0.35},
    "mustard": {"initial": 0.35, "mid": 1.10, "late": 0.30},
    "pulses": {"initial": 0.40, "mid": 1.15, "late": 0.35},
    "gram": {"initial": 0.40, "mid": 1.15, "late": 0.35},
    "barley": {"initial": 0.30, "mid": 1.15, "late": 0.25},
    "default": {"initial": 0.40, "mid": 1.15, "late": 0.40}
}


class HydrologyEngine:
    """Standard FAO-56 and PyET-compliant evapotranspiration and deficit engine."""

    def calculate_extraterrestrial_radiation(self, latitude_deg: float, doy: int) -> float:
        """
        Calculates daily extraterrestrial radiation Ra (MJ/m^2/day) based on solar geometry.
        Matches FAO-56 Equation 21 / PyET formulation.
        """
        phi = math.radians(latitude_deg)
        dr = 1.0 + 0.033 * math.cos(2.0 * math.pi * doy / 365.0)
        delta = 0.409 * math.sin((2.0 * math.pi * doy / 365.0) - 1.39)
        
        # Sunset hour angle
        tan_term = -math.tan(phi) * math.tan(delta)
        tan_term = max(-1.0, min(1.0, tan_term))
        omega_s = math.acos(tan_term)
        
        g_sc = 0.0820  # Solar constant MJ/m^2/min
        ra = (24.0 * 60.0 / math.pi) * g_sc * dr * (
            omega_s * math.sin(phi) * math.sin(delta) +
            math.cos(phi) * math.cos(delta) * math.sin(omega_s)
        )
        return max(0.0, ra)

    def calculate_et0_hargreaves(
        self, 
        t_min: np.ndarray, 
        t_max: np.ndarray, 
        ra: np.ndarray,
        latitude_deg: float = 30.638
    ) -> np.ndarray:
        """
        Hargreaves-Samani Reference Evapotranspiration (ETo in mm/day).
        Executes through pyet.hargreaves (FAO-56 standard implementation).
        """
        if _PYET_AVAILABLE:
            try:
                lat_rad = math.radians(latitude_deg)
                tmin_s = pd.Series(t_min.flatten())
                tmax_s = pd.Series(t_max.flatten())
                tmean_s = (tmin_s + tmax_s) / 2.0
                et0_res = pyet.hargreaves(tmean_s, tmax_s, tmin_s, lat=lat_rad)
                return np.array(et0_res.values).reshape(t_min.shape)
            except Exception:
                pass
        t_mean = (t_min + t_max) / 2.0
        t_diff = np.maximum(t_max - t_min, 0.0)
        et0 = 0.0023 * (t_mean + 17.8) * np.sqrt(t_diff) * (ra / 2.45)
        return np.maximum(et0, 0.0)

    def get_crop_kc(self, crop_type: str, stage: str) -> float:
        """Retrieves exact FAO-56 crop coefficient Kc based on crop species and growth phase."""
        key = "default"
        crop_lower = crop_type.lower()
        for k in FAO56_KC_TABLE:
            if k in crop_lower:
                key = k
                break
        
        stage_lower = stage.lower()
        if any(s in stage_lower for s in ["veg", "init", "till", "emerg", "cri", "root"]):
            return FAO56_KC_TABLE[key]["initial"]
        elif any(s in stage_lower for s in ["flow", "mid", "head", "boll", "pod", "boot"]):
            return FAO56_KC_TABLE[key]["mid"]
        else:
            return FAO56_KC_TABLE[key]["late"]

    def compute_usda_effective_rainfall(self, p_total_8day: float) -> float:
        """
        USDA Soil Conservation Service (SCS) formula for 8-day effective precipitation (mm).
        P_eff accounts for runoff and deep percolation losses.
        """
        if p_total_8day <= 0:
            return 0.0
        if p_total_8day <= 125.0:
            p_eff = p_total_8day * (125.0 - 0.2 * p_total_8day) / 125.0
        else:
            p_eff = 125.0 / 3.0 + 0.1 * p_total_8day
        return max(0.0, float(p_eff))

    def compute_8day_water_deficit(
        self,
        et0_daily: float,
        kc: float,
        p_total_8day: float,
        soil_moisture_fraction: float = 0.50
    ) -> Dict[str, float]:
        """
        Computes 8-day actual crop evapotranspiration, effective rainfall, and net water deficit.
        """
        et0_8day = et0_daily * 8.0
        et_c = et0_8day * kc
        p_eff = self.compute_usda_effective_rainfall(p_total_8day)
        
        # Actual evapotranspiration (ETa) constrained by root-zone soil moisture availability
        # FAO-56 water stress coefficient Ks = (SMI - WP) / (FC - WP)
        wilting_point = 0.15
        field_capacity = 0.70
        ks = np.clip((soil_moisture_fraction - wilting_point) / (field_capacity - wilting_point), 0.10, 1.0)
        et_a = et_c * float(ks)
        
        # Net hydrological water deficit (mm depth over 8 days)
        # Deficit = max(0, ETc - ETa - Peff)
        deficit_mm = max(0.0, et_c - et_a - (p_eff * 0.5))
        
        return {
            "et0_8day": round(et0_8day, 1),
            "kc": round(kc, 2),
            "et_c": round(et_c, 1),
            "et_a": round(et_a, 1),
            "p_eff": round(p_eff, 1),
            "deficit_mm": round(deficit_mm, 1)
        }


def compute_block_water_deficit(
    block_id: str, 
    area_ha: float, 
    crop_type: str, 
    stage: str,
    smi_sar: float = 0.45,
    t_min: float = 14.5,
    t_max: float = 28.2,
    ra: float = 22.4,
    p_total_8day: float = 4.0
) -> Dict[str, Any]:
    """
    Computes rigorous hydrological deficit and canal gate discharge release recommendations.
    """
    engine = HydrologyEngine()
    
    # 1. Compute Hargreaves ETo from daily temperature and solar radiation
    et0_arr = engine.calculate_et0_hargreaves(
        np.array([t_min]), np.array([t_max]), np.array([ra])
    )
    et0_daily = float(et0_arr[0])
    
    # 2. Get exact FAO-56 Crop Coefficient Kc
    kc = engine.get_crop_kc(crop_type, stage)
    
    # 3. Compute 8-day water balance
    balance = engine.compute_8day_water_deficit(
        et0_daily=et0_daily,
        kc=kc,
        p_total_8day=p_total_8day,
        soil_moisture_fraction=smi_sar
    )
    deficit_mm = balance["deficit_mm"]
    
    # 4. Volumetric water demand: 1 mm depth = 10 m^3/ha
    volumetric_deficit_m3 = deficit_mm * 10.0 * area_ha
    
    # 5. Sluice gate continuous discharge (Q = V / (t * eta_conveyance))
    # 8 days = 192 hours = 691,200 seconds; field canal conveyance efficiency eta = 0.72
    seconds_8day = 8 * 24 * 3600
    discharge_cumecs = volumetric_deficit_m3 / (seconds_8day * 0.72)
    
    # 6. Agronomic Moisture Stress Classification
    if deficit_mm < 6.0:
        stress_category = "Normal"
    elif deficit_mm < 16.0:
        stress_category = "Mild"
    elif deficit_mm < 28.0:
        stress_category = "Moderate"
    else:
        stress_category = "Severe"
        
    return {
        "block_id": block_id,
        "crop_type": crop_type,
        "stage": stage,
        "et0_8day_mm": balance["et0_8day"],
        "kc": balance["kc"],
        "et_c_mm": balance["et_c"],
        "et_a_mm": balance["et_a"],
        "p_eff_mm": balance["p_eff"],
        "deficit_mm": deficit_mm,
        "volumetric_deficit_m3": round(volumetric_deficit_m3, 1),
        "recommended_discharge_cumecs": round(discharge_cumecs, 3),
        "stress_category": stress_category
    }
