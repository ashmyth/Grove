import torch
import numpy as np
from backend.model import MSFNetCropClassifier, RandomForestCropClassifier, run_crop_inference

def test_msf_net_dimensions():
    model = MSFNetCropClassifier(num_classes=5)
    model.eval()
    
    # Mock optical tensor: (Batch=2, T=3, C=6, H=224, W=224)
    optical = torch.randn(2, 3, 6, 224, 224)
    # Mock SAR tensor: (Batch=2, C=2, H=11, W=11)
    sar = torch.randn(2, 2, 11, 11)
    
    with torch.no_grad():
        outputs = model(optical, sar)
        
    assert "logits_fused" in outputs
    assert "logits_optical" in outputs
    assert "logits_sar" in outputs
    
    assert outputs["logits_fused"].shape == (2, 5)
    assert outputs["logits_optical"].shape == (2, 5)
    assert outputs["logits_sar"].shape == (2, 5)

def test_msf_net_radar_fallback():
    model = MSFNetCropClassifier(num_classes=5)
    model.eval()
    
    # Simulate fully clouded/missing optical data (all NaNs)
    optical = torch.full((2, 3, 6, 224, 224), float('nan'))
    sar = torch.randn(2, 2, 11, 11)
    
    with torch.no_grad():
        outputs = model(optical, sar)
        
    # Since optical was NaN, the fused output should just rely on SAR, no NaNs should propagate
    assert not torch.isnan(outputs["logits_fused"]).any()
    assert outputs["logits_fused"].shape == (2, 5)

def test_random_forest_fallback():
    # Test scikit-learn CPU fallback
    rf = RandomForestCropClassifier()
    # Mock dataset: 10 samples, 20 features
    X = np.random.rand(10, 20)
    y = np.random.randint(0, 5, 10)
    
    rf.fit(X, y)
    preds = rf.predict(X)
    
    assert preds.shape == (10,)
    assert set(preds).issubset({0, 1, 2, 3, 4})

def test_run_crop_inference_interface():
    optical = torch.randn(3, 6, 224, 224)
    sar = torch.randn(2, 11, 11)
    
    preds = run_crop_inference(optical, sar)
    
    assert isinstance(preds, np.ndarray)
    assert preds.shape == (10, 10)
