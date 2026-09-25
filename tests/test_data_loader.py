"""
Unit tests for Teammate 1: Data Pipeline & Data Loader
Verifies Interface 1 compliance and memory-mapped dataset functionality.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.data_loader import load_feature_tensors, GroveDataset
from backend.gee_pipeline import EE_AVAILABLE, initialize_gee


def test_interface_1_contract():
    """Verifies Interface 1 return dictionary keys and shapes."""
    result = load_feature_tensors("sample_001")
    
    assert "optical_tensor" in result, "Missing optical_tensor in Interface 1 dict"
    assert "sar_patch" in result, "Missing sar_patch in Interface 1 dict"
    assert "dem_slope" in result, "Missing dem_slope in Interface 1 dict"
    assert "era5_meteo" in result, "Missing era5_meteo in Interface 1 dict"
    assert "metadata" in result, "Missing metadata in Interface 1 dict"
    
    opt = result["optical_tensor"]
    sar = result["sar_patch"]
    
    opt_shape = tuple(opt.shape)
    sar_shape = tuple(sar.shape)
    
    assert opt_shape == (1, 3, 6, 224, 224), f"Unexpected optical_tensor shape: {opt_shape}"
    assert sar_shape == (1, 2, 11, 11), f"Unexpected sar_patch shape: {sar_shape}"
    
    meteo = result["era5_meteo"]
    assert "t_min" in meteo and "t_max" in meteo and "p_total" in meteo, "Incomplete meteorology keys"
    
    print("[OK] Interface 1 Contract Verification Passed!")


def test_grove_dataset():
    """Verifies PyTorch / NumPy GroveDataset indexing."""
    dataset = GroveDataset(file_paths=["sample_001", "sample_002"])
    assert len(dataset) == 2, f"Expected dataset len 2, got {len(dataset)}"
    
    item = dataset[0]
    opt_shape = tuple(item["optical_tensor"].shape)
    sar_shape = tuple(item["sar_patch"].shape)
    
    assert opt_shape == (3, 6, 224, 224), f"Unexpected squeezed optical shape: {opt_shape}"
    assert sar_shape == (2, 11, 11), f"Unexpected squeezed sar shape: {sar_shape}"
    
    print("[OK] GroveDataset Verification Passed!")


def test_gee_pipeline_graceful():
    """Verifies GEE pipeline initialization and fallback handling."""
    res = initialize_gee()
    assert isinstance(res, bool)
    print(f"[OK] GEE Pipeline Verification Passed! (EE_AVAILABLE={EE_AVAILABLE})")


if __name__ == '__main__':
    test_interface_1_contract()
    test_grove_dataset()
    test_gee_pipeline_graceful()
    print("\n[ALL TEAMMATE 1 TESTS PASSED SUCCESSFULLY]")
