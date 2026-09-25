import numpy as np
from typing import Dict, Tuple

try:
    from scipy.signal import savgol_filter
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    def savgol_filter(x, window_length, polyorder):
        # Graceful pure numpy rolling average fallback when scipy is not yet installed
        kernel_size = min(len(x), window_length)
        if kernel_size <= 1:
            return np.array(x)
        kernel = np.ones(kernel_size) / kernel_size
        return np.convolve(x, kernel, mode='same')


class PhenologyStressEngine:
    def __init__(self, window_length: int = 5, polyorder: int = 2):
        self.window_length = window_length
        self.polyorder = polyorder

    def compute_phenology_markers(self, ndvi_timeseries: np.ndarray, doy_vector: np.ndarray) -> Dict[str, int]:
        """
        Extracts SOS (Start of Season), Peak Vegetative, and LGP (Length of Growing Period).
        Uses Savitzky-Golay polynomial smoothing.
        """
        # Edge case: if timeseries is shorter than window length
        if len(ndvi_timeseries) < self.window_length:
            wl = max(3, len(ndvi_timeseries)) if len(ndvi_timeseries) >= 3 else 1
            # For short sequences, smooth with adaptive window or return raw series
            if wl > 1 and wl % 2 == 0: wl -= 1
            smoothed_ndvi = savgol_filter(ndvi_timeseries, wl, min(self.polyorder, wl-1)) if wl > 1 else ndvi_timeseries
        else:
            smoothed_ndvi = savgol_filter(ndvi_timeseries, self.window_length, self.polyorder)

        if len(smoothed_ndvi) == 0:
            return {"sos_doy": 0, "peak_doy": 0, "lgp_days": 0}

        # Find Peak Vegetative
        peak_idx = np.argmax(smoothed_ndvi)
        peak_doy = int(doy_vector[peak_idx])

        # Estimate SOS (Start of Season): e.g., 20% of max amplitude before peak
        max_val = smoothed_ndvi[peak_idx]
        min_val = np.min(smoothed_ndvi[:peak_idx+1]) if peak_idx > 0 else 0
        threshold = min_val + 0.2 * (max_val - min_val)
        
        sos_idx = 0
        for i in range(peak_idx, -1, -1):
            if smoothed_ndvi[i] <= threshold:
                sos_idx = i
                break
        
        sos_doy = int(doy_vector[sos_idx])

        # Estimate EOS (End of Season) and LGP
        eos_idx = len(smoothed_ndvi) - 1
        for i in range(peak_idx, len(smoothed_ndvi)):
            if smoothed_ndvi[i] <= threshold:
                eos_idx = i
                break
                
        eos_doy = int(doy_vector[eos_idx])
        lgp_days = max(0, eos_doy - sos_doy)

        return {
            "sos_doy": sos_doy,
            "peak_doy": peak_doy,
            "lgp_days": lgp_days
        }

    def evaluate_stress_ensemble(
        self, 
        vci: np.ndarray, 
        smi: np.ndarray, 
        lst_anomaly: np.ndarray, 
        stage: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the Composite Moisture Stress Index (CMSI).
        stage-dependent weights:
        - Vegetative: VCI=0.2, SMI=0.6, LST=0.2
        - Flowering: VCI=0.35, SMI=0.35, LST=0.30
        - Ripening: VCI=0.5, SMI=0.3, LST=0.2
        
        Returns (composite_stress_score [0..100], stress_category_enum).
        """
        if stage.lower() == "vegetative":
            w_vci, w_smi, w_lst = 0.2, 0.6, 0.2
        elif stage.lower() == "flowering":
            w_vci, w_smi, w_lst = 0.35, 0.35, 0.30
        elif stage.lower() == "ripening":
            w_vci, w_smi, w_lst = 0.5, 0.3, 0.2
        else: # Default
            w_vci, w_smi, w_lst = 0.33, 0.33, 0.34
            
        tai_clipped = np.clip(lst_anomaly * 20, 0, 100)
        
        cmsi = w_vci * (100 - vci) + w_smi * (100 - smi) + w_lst * tai_clipped
        cmsi = np.clip(cmsi, 0, 100)
        
        # Categorize
        categories = np.empty_like(cmsi, dtype=object)
        categories[cmsi < 25] = "Normal"
        categories[(cmsi >= 25) & (cmsi < 50)] = "Mild"
        categories[(cmsi >= 50) & (cmsi < 75)] = "Moderate"
        categories[cmsi >= 75] = "Severe"
        
        return cmsi, categories
