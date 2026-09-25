import numpy as np
from typing import Dict

class HydrologyEngine:
    def calculate_et0_hargreaves(self, t_min: np.ndarray, t_max: np.ndarray, ra: np.ndarray) -> np.ndarray:
        """
        Computes daily Reference Evapotranspiration (ETo) in mm/day using Hargreaves-Samani equation.
        ETo = 0.0023 * (T_avg + 17.8) * (T_max - T_min)^0.5 * (Ra / 2.45)
        """
        t_avg = (t_min + t_max) / 2.0
        # Prevent negative sqrt
        t_diff = np.maximum(t_max - t_min, 0.0)
        
        # Ra is Extraterrestrial radiation in MJ/m2/day. 
        # Divided by 2.45 to convert MJ/m2/day to mm/day equivalent of latent heat of vaporization
        et0 = 0.0023 * (t_avg + 17.8) * np.sqrt(t_diff) * (ra / 2.45)
        return np.maximum(et0, 0.0)

    def compute_8day_water_deficit(
        self, 
        et0_8day: np.ndarray, 
        kc_stage: np.ndarray, 
        actual_et: np.ndarray, 
        p_total_8day: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """
        Computes effective rainfall, crop evapotranspiration, and 8-day water deficit.
        """
        # Effective rainfall: Peff = 0.8 * Ptotal - 5 for Ptotal > 10, else 0
        p_eff = np.where(p_total_8day > 10, 0.8 * p_total_8day - 5, 0.0)
        p_eff = np.maximum(p_eff, 0.0)
        
        # Crop evapotranspiration (ETc)
        et_c = et0_8day * kc_stage
        
        # Deficit_8 = max(0, ETc - ETa - Peff)
        deficit_mm = np.maximum(0.0, et_c - actual_et - p_eff)
        
        return {
            "p_eff_8day": p_eff,
            "et_c": et_c,
            "deficit_mm": deficit_mm
        }

def compute_block_water_deficit(block_id: str, area_ha: float, crop_type: str, stage: str) -> dict:
    """
    Interface Contract 2: ML / Hydrology -> FastAPI Backend
    """
    # Mocking real environmental variables for this specific block
    engine = HydrologyEngine()
    
    # Mock data: 8 days of 5 mm/day ET0 = 40 mm
    et0_mock = np.array([40.0])
    
    # Stage dependent Kc mock
    if stage.lower() == "vegetative":
        kc = np.array([0.5])
    elif stage.lower() == "flowering":
        kc = np.array([1.1])
    else:
        kc = np.array([0.7])
        
    actual_et_mock = np.array([10.0])
    p_total_mock = np.array([15.0]) # Should yield Peff = 0.8*15 - 5 = 7.0
    
    results = engine.compute_8day_water_deficit(et0_mock, kc, actual_et_mock, p_total_mock)
    
    deficit_mm = float(results["deficit_mm"][0])
    
    # Volumetric requirement: V = Deficit * 10 * Area_ha (since 1mm = 10 m3/ha)
    volumetric_deficit_m3 = deficit_mm * 10.0 * area_ha
    
    # Sluice discharge: Q = V / (t * 3600 * 0.7)
    # Assume t = 8 days = 192 hours
    # 0.70 is conveyance efficiency
    t_hours = 192
    discharge_cumecs = volumetric_deficit_m3 / (t_hours * 3600 * 0.70)
    
    # Determine stress category arbitrarily based on deficit
    if deficit_mm < 5:
        category = "Normal"
    elif deficit_mm < 15:
        category = "Mild"
    elif deficit_mm < 25:
        category = "Moderate"
    else:
        category = "Severe"
        
    return {
        "block_id": block_id,
        "crop_type": crop_type,
        "stage": stage.capitalize(),
        "deficit_mm": round(deficit_mm, 2),
        "volumetric_deficit_m3": round(volumetric_deficit_m3, 2),
        "recommended_discharge_cumecs": round(discharge_cumecs, 3),
        "stress_category": category
    }
