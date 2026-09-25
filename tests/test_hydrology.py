import numpy as np
from backend.hydrology import HydrologyEngine, compute_block_water_deficit

def test_hargreaves_et0():
    engine = HydrologyEngine()
    
    t_min = np.array([18.0])
    t_max = np.array([32.0])
    ra = np.array([15.2]) # MJ/m2/day
    
    et0 = engine.calculate_et0_hargreaves(t_min, t_max, ra)
    
    assert et0.shape == (1,)
    # Verify calculation: 
    # et0 = 0.0023 * (25.0 + 17.8) * sqrt(14.0) * (15.2 / 2.45)
    # et0 = 0.0023 * 42.8 * 3.7416 * 6.204
    # et0 ~= 2.28 mm/day
    assert abs(et0[0] - 2.28) < 0.1

def test_effective_rainfall():
    engine = HydrologyEngine()
    
    # Test cases: <10mm, exactly 10mm, >10mm
    p_total = np.array([5.0, 10.0, 15.0])
    
    # et0_8day, kc, actual_et are mocked
    et0 = np.array([40.0, 40.0, 40.0])
    kc = np.array([1.0, 1.0, 1.0])
    actual_et = np.array([10.0, 10.0, 10.0])
    
    results = engine.compute_8day_water_deficit(et0, kc, actual_et, p_total)
    
    p_eff = results["p_eff_8day"]
    # expected:
    # 5.0 -> <= 10 -> 0.0
    # 10.0 -> <= 10 -> 0.0
    # 15.0 -> > 10 -> 0.8 * 15 - 5 = 7.0
    np.testing.assert_array_almost_equal(p_eff, [0.0, 0.0, 7.0])

def test_water_deficit_logic():
    engine = HydrologyEngine()
    
    et0 = np.array([50.0])
    kc = np.array([1.2]) # ETc = 60.0
    actual_et = np.array([20.0])
    p_total = np.array([20.0]) # Peff = 16 - 5 = 11.0
    
    results = engine.compute_8day_water_deficit(et0, kc, actual_et, p_total)
    deficit = results["deficit_mm"]
    
    # Deficit = max(0, ETc - ETa - Peff) = 60 - 20 - 11 = 29.0
    np.testing.assert_array_almost_equal(deficit, [29.0])

def test_interface_compute_block_water_deficit():
    res = compute_block_water_deficit(
        block_id="CANAL_B1",
        area_ha=50.0,
        crop_type="Paddy",
        stage="Flowering"
    )
    
    assert res["block_id"] == "CANAL_B1"
    assert res["crop_type"] == "Paddy"
    assert res["stage"] == "Flowering"
    assert isinstance(res["deficit_mm"], float)
    assert isinstance(res["volumetric_deficit_m3"], float)
    assert isinstance(res["recommended_discharge_cumecs"], float)
    assert isinstance(res["stress_category"], str)
