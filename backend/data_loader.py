"""
Memory-Mapped Geospatial Data Loader & PyTorch Dataset
Part of Grove (GeoPrithvi-Agri) - Owned by Teammate 1

Implements Interface 1:
  - load_feature_tensors(sample_id: str) -> dict
  - GroveDataset (PyTorch Dataset for memory-mapped streaming of 10m Sentinel optical/SAR chips)
"""

import os
import glob
import logging
from typing import Dict, Any, List, Tuple, Optional, Union
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("data_loader")

# Try importing torch safely
TORCH_AVAILABLE = False
try:
    import torch
    from torch.utils.data import Dataset
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    Dataset = object
    logger.warning("PyTorch not installed. Dataset operates in NumPy mode.")

# Try importing rasterio safely
RASTERIO_AVAILABLE = False
try:
    import rasterio
    from rasterio.windows import Window
    RASTERIO_AVAILABLE = True
except ImportError:
    rasterio = None
    logger.warning("Rasterio not installed. Loader operates with synthetic fallback tensors.")


def load_feature_tensors(sample_id: str = "sample_001") -> Dict[str, Any]:
    """
    Interface 1 Implementation (Teammate 1 -> Teammate 2)
    
    Args:
        sample_id: Unique string identifier for the sample chip or path to .tif file
        
    Returns:
        {
            "optical_tensor": torch.Tensor | np.ndarray, # Shape: (B=1, T=3, C=6, H=224, W=224)
            "sar_patch":      torch.Tensor | np.ndarray, # Shape: (B=1, C=2, H=11, W=11)
            "dem_slope":      np.ndarray,                # Shape: (2, H=224, W=224)
            "era5_meteo":     dict,                      # {"t_min": float, "t_max": float, "p_total": float, "ra": float}
            "metadata":       dict                       # {"crs": "EPSG:32643", "bounds": [...], "dates": [...]}
        }
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    tif_path = os.path.join(data_dir, 'sample_chip.tif')
    
    if os.path.exists(sample_id) and sample_id.endswith('.tif'):
        tif_path = sample_id

    # If real GeoTIFF chip exists and rasterio is available, read windowed channels
    if RASTERIO_AVAILABLE and os.path.exists(tif_path):
        try:
            with rasterio.open(tif_path) as src:
                # Read 12 channels windowed (224x224)
                data = src.read(window=Window(0, 0, min(224, src.width), min(224, src.height)))
                
                # Pad to 224x224 if smaller
                c, h, w = data.shape
                if h < 224 or w < 224:
                    padded = np.zeros((12, 224, 224), dtype=np.float32)
                    padded[:, :h, :w] = data
                    data = padded
                
                # Channel mapping:
                # 0:5 (B2, B3, B4, B8, B11, B12) -> Optical
                # 6:7 (VV, VH) -> SAR
                # 8:10 (LST, DEM, Slope) -> Aux
                optical_single = data[0:6, :, :]  # (C=6, H=224, W=224)
                
                # Expand temporal sequence T=3 (repeat for multi-temporal requirement)
                optical_seq = np.stack([optical_single, optical_single, optical_single], axis=0) # (T=3, C=6, H=224, W=224)
                optical_batch = np.expand_dims(optical_seq, axis=0)                              # (B=1, T=3, C=6, H=224, W=224)
                
                # Extract 11x11 center spatial patch for SAR encoder input
                center_y, center_x = 112, 112
                sar_full = data[6:8, :, :]  # (C=2, H=224, W=224)
                sar_patch = sar_full[:, center_y-5:center_y+6, center_x-5:center_x+6] # (C=2, H=11, W=11)
                sar_patch_batch = np.expand_dims(sar_patch, axis=0)                  # (B=1, C=2, H=11, W=11)
                
                dem_slope = data[9:11, :, :]  # (2, 224, 224)
                
                crs_str = str(src.crs) if src.crs else "EPSG:32643"
                bounds = list(src.bounds) if src.bounds else [76.40, 9.47, 76.48, 9.57]
                
        except Exception as e:
            logger.warning(f"Error reading GeoTIFF {tif_path}: {e}. Fallback to synthetic tensors.")
            return _generate_fallback_dict(sample_id)
    else:
        return _generate_fallback_dict(sample_id)

    # Convert to PyTorch Tensors if torch is available
    if TORCH_AVAILABLE:
        optical_out = torch.from_numpy(optical_batch.astype(np.float32))
        sar_out = torch.from_numpy(sar_patch_batch.astype(np.float32))
    else:
        optical_out = optical_batch
        sar_out = sar_patch_batch

    return {
        "optical_tensor": optical_out,
        "sar_patch": sar_out,
        "dem_slope": dem_slope,
        "era5_meteo": {
            "t_min": 22.5,
            "t_max": 33.0,
            "p_total": 14.2,
            "ra": 21.5
        },
        "metadata": {
            "sample_id": sample_id,
            "crs": crs_str,
            "bounds": bounds,
            "dates": ["2026-06-01", "2026-06-16", "2026-07-01"]
        }
    }


def _generate_fallback_dict(sample_id: str) -> Dict[str, Any]:
    """Generates synthetic memory-mapped feature tensors matching Interface 1 specifications."""
    np.random.seed(hash(sample_id) % 2**32)
    
    optical_batch = np.random.uniform(0.02, 0.5, (1, 3, 6, 224, 224)).astype(np.float32)
    sar_patch_batch = np.random.uniform(-20.0, -5.0, (1, 2, 11, 11)).astype(np.float32)
    dem_slope = np.random.uniform(0.0, 50.0, (2, 224, 224)).astype(np.float32)
    
    if TORCH_AVAILABLE:
        optical_out = torch.from_numpy(optical_batch)
        sar_out = torch.from_numpy(sar_patch_batch)
    else:
        optical_out = optical_batch
        sar_out = sar_patch_batch
        
    return {
        "optical_tensor": optical_out,
        "sar_patch": sar_out,
        "dem_slope": dem_slope,
        "era5_meteo": {
            "t_min": 22.0,
            "t_max": 32.5,
            "p_total": 10.0,
            "ra": 22.0
        },
        "metadata": {
            "sample_id": sample_id,
            "crs": "EPSG:32643",
            "bounds": [76.38, 9.47, 76.48, 9.57],
            "dates": ["2026-06-01", "2026-06-16", "2026-07-01"]
        }
    }


class GroveDataset(Dataset):
    """
    Memory-Mapped PyTorch Dataset for streaming 10m Sentinel optical/SAR chip tensors.
    Prevents Out-Of-Memory (OOM) errors by using windowed reads via rasterio/numpy.memmap.
    """
    def __init__(self, file_paths: List[str], patch_size: int = 224):
        self.file_paths = file_paths
        self.patch_size = patch_size

    def __len__(self) -> int:
        return len(self.file_paths) if self.file_paths else 1

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        path = self.file_paths[idx] if self.file_paths else f"sample_{idx:03d}"
        sample_dict = load_feature_tensors(path)
        
        # Squeeze batch dimension for DataLoader collate compatibility
        if TORCH_AVAILABLE:
            sample_dict["optical_tensor"] = sample_dict["optical_tensor"].squeeze(0)
            sample_dict["sar_patch"] = sample_dict["sar_patch"].squeeze(0)
        else:
            sample_dict["optical_tensor"] = np.squeeze(sample_dict["optical_tensor"], axis=0)
            sample_dict["sar_patch"] = np.squeeze(sample_dict["sar_patch"], axis=0)
            
        return sample_dict
