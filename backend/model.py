import torch
import torch.nn as nn
import numpy as np
from typing import Dict
from sklearn.ensemble import RandomForestClassifier

class PrithviFeatureExtractor(nn.Module):
    def __init__(self):
        super().__init__()
        # Mocking the frozen Prithvi-100M ViT backbone for now to avoid downloading massive weights
        # In production, this would be: transformers.AutoModel.from_pretrained('ibm-nasa-geospatial/Prithvi-100M')
        self.fc = nn.Linear(6 * 224 * 224, 256)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape expected: (B, T, C, H, W). We flatten for mock.
        B = x.size(0)
        x_flat = x.view(B, -1)
        # Mock downsampling to 256-dim embeddings
        out = self.fc(x_flat[:, :6*224*224])
        return out

class SARPatchEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        # 2D CNN with residual blocks for 11x11 SAR patches (C=2)
        self.conv1 = nn.Conv2d(2, 64, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(128, 256)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (B, 2, 11, 11)
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

class MSFNetCropClassifier(nn.Module):
    def __init__(self, num_classes: int = 5):
        super().__init__()
        self.optical_extractor = PrithviFeatureExtractor()
        self.sar_extractor = SARPatchEncoder()
        
        # Late-fusion MLP head
        self.mlp = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        
        # Auxiliary loss heads
        self.opt_head = nn.Linear(256, num_classes)
        self.sar_head = nn.Linear(256, num_classes)

    def forward(self, optical_seq: torch.Tensor, sar_patches: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        optical_seq: (B, T, C=6, H=224, W=224)
        sar_patches: (B, C=2, H=11, W=11)
        """
        # Feature extraction
        f_opt = self.optical_extractor(optical_seq)
        f_sar = self.sar_extractor(sar_patches)
        
        # Automated fallback: if optical is NaN or empty (simulated by checking if all 0/nan)
        if torch.isnan(optical_seq).any() or optical_seq.sum() == 0:
            # Fallback to SAR only
            f_fused = f_sar
        else:
            # Late-fusion vector addition
            f_fused = f_opt + f_sar
            
        logits_fused = self.mlp(f_fused)
        logits_optical = self.opt_head(f_opt)
        logits_sar = self.sar_head(f_sar)
        
        return {
            "logits_fused": logits_fused,
            "logits_optical": logits_optical,
            "logits_sar": logits_sar
        }

class RandomForestCropClassifier:
    def __init__(self):
        self.rf = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def fit(self, X: np.ndarray, y: np.ndarray):
        self.rf.fit(X, y)
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.rf.predict(X)

def run_crop_inference(optical_tensor: torch.Tensor, sar_patch: torch.Tensor) -> np.ndarray:
    """
    Interface Contract 2: ML / Hydrology -> FastAPI Backend
    Returns 2D integer array (H, W) where 0=Paddy, 1=Cotton, 2=Maize, 3=Sugarcane, 4=Pulses
    """
    # Assuming (H, W) for output grid based on some patch processing.
    # For this mock implementation, we'll return a 10x10 mock grid of class predictions.
    # A real implementation would reconstruct the (H, W) grid from the batched outputs.
    model = MSFNetCropClassifier(num_classes=5)
    model.eval()
    
    # Expand dims if single sample
    if len(optical_tensor.shape) == 4:
        optical_tensor = optical_tensor.unsqueeze(0)
    if len(sar_patch.shape) == 3:
        sar_patch = sar_patch.unsqueeze(0)
        
    with torch.no_grad():
        outputs = model(optical_tensor, sar_patch)
        logits = outputs["logits_fused"]
        preds = torch.argmax(logits, dim=1).numpy()
    
    # Mocking returning a 10x10 grid with the predicted class filling it
    pred_class = preds[0] if len(preds) > 0 else 0
    return np.full((10, 10), pred_class, dtype=int)
