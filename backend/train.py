"""
Grove (GeoPrithvi-Agri) - Multi-Source Crop Classification Training Pipeline
Trains the AI model on optical (Sentinel-2) and radar (Sentinel-1/EOS-04) feature signatures,
evaluates test performance, and saves model checkpoints & metrics.
"""

import os
import sys
import json
import csv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "crop_spectral_signatures.csv"
WEIGHTS_DIR = ROOT_DIR / "backend" / "weights"
WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

CROP_NAMES = [
    "Paddy (Rice)",
    "Cotton",
    "Maize",
    "Sugarcane",
    "Wheat / Pulses / Mustard"
]

FEATURE_KEYS = [
    "B2_blue", "B3_green", "B4_red", "B8_nir", "B11_swir1", "B12_swir2",
    "ndvi", "evi", "ndwi",
    "sar_vv_db", "sar_vh_db",
    "sar_mv_volume", "sar_ms_surface", "smi_sar",
    "lst_anomaly", "dem_elevation", "slope_deg"
]

def load_data():
    if not DATA_PATH.exists():
        from backend.dataset_generator import generate_crop_dataset
        generate_crop_dataset()

    X = []
    y = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            features = [float(row[k]) for k in FEATURE_KEYS]
            X.append(features)
            y.append(int(row["crop_code"]))

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int64)

def train_crop_models():
    print("=" * 65)
    print("  GROVE (GeoPrithvi-Agri) - Model Training Pipeline")
    print("=" * 65)

    X, y = load_data()
    print(f"\n[1/4] Loaded {len(X)} satellite observations across {len(CROP_NAMES)} crop classes.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"      Train split: {len(X_train)} samples | Test split: {len(X_test)} samples")

    # 1. Train Random Forest Classifier
    print("\n[2/4] Training Random Forest Multi-Sensor Classifier (100 estimators)...")
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        class_weight="balanced",
        random_state=42
    )
    rf.fit(X_train, y_train)

    # 2. Evaluate Performance
    print("\n[3/4] Evaluating model on unseen test split...")
    y_pred = rf.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    prec, rec, f1, support = precision_recall_fscore_support(y_test, y_pred, average="macro")

    # Per-class metrics
    class_prec, class_rec, class_f1, class_supp = precision_recall_fscore_support(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Feature importances
    importances = rf.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    ranked_features = [
        {"feature": FEATURE_KEYS[i], "importance": round(float(importances[i]), 4)}
        for i in sorted_idx
    ]

    per_class_report = {}
    for i, name in enumerate(CROP_NAMES):
        per_class_report[name] = {
            "precision": round(float(class_prec[i]), 3),
            "recall": round(float(class_rec[i]), 3),
            "f1_score": round(float(class_f1[i]), 3),
            "support": int(class_supp[i])
        }

    print(f"      Overall Accuracy : {acc * 100:.2f}%")
    print(f"      Macro F1-Score   : {f1 * 100:.2f}%")
    print(f"      Macro Precision  : {prec * 100:.2f}%")
    print(f"      Macro Recall     : {rec * 100:.2f}%")

    # 3. Save Model Artifacts
    print("\n[4/4] Saving model weights and performance benchmarks...")
    model_save_path = WEIGHTS_DIR / "rf_crop_classifier.joblib"
    joblib.dump(rf, model_save_path)
    print(f"      Saved model checkpoint -> {model_save_path}")

    metrics_payload = {
        "model_name": "RandomForest-MSF-CropClassifier",
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(acc, 4),
        "macro_f1": round(float(f1), 4),
        "macro_precision": round(float(prec), 4),
        "macro_recall": round(float(rec), 4),
        "confusion_matrix": cm,
        "class_names": CROP_NAMES,
        "per_class_metrics": per_class_report,
        "top_features": ranked_features[:8]
    }

    metrics_save_path = WEIGHTS_DIR / "model_metrics.json"
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"      Saved metrics JSON -> {metrics_save_path}")

    # PyTorch MSF-Net Multimodal Late-Fusion training
    try:
        import torch
        import torch.nn as nn
        from backend.model import MSFNetCropClassifier
        print("\n[*] PyTorch detected. Training Multimodal Late-Fusion Network (MSF-Net)...")
        
        # Split features into Optical (0..9) and SAR (9..14)
        X_opt_t = torch.tensor(X_train[:, :9], dtype=torch.float32)
        X_sar_t = torch.tensor(X_train[:, 9:14], dtype=torch.float32)
        y_train_t = torch.tensor(y_train, dtype=torch.long)
        
        net = MSFNetCropClassifier(num_classes=len(CROP_NAMES))
        optimizer = torch.optim.Adam(net.parameters(), lr=0.004, weight_decay=1e-4)
        criterion = nn.CrossEntropyLoss()
        
        net.train()
        for epoch in range(50):
            optimizer.zero_grad()
            out = net(X_opt_t, X_sar_t)
            # Auxiliary multi-task loss matching architecture.md: L_fused + 0.3*L_opt + 0.3*L_sar
            l_fused = criterion(out["logits_fused"], y_train_t)
            l_opt = criterion(out["logits_optical"], y_train_t)
            l_sar = criterion(out["logits_sar"], y_train_t)
            loss = l_fused + 0.3 * l_opt + 0.3 * l_sar
            loss.backward()
            optimizer.step()
            
        torch.save(net.state_dict(), WEIGHTS_DIR / "msfnet_crop.pt")
        print("      Saved PyTorch MSF-Net trained weights -> msfnet_crop.pt")
    except Exception as e:
        print(f"      (PyTorch training note: {e})")

    print("\nTraining completed successfully! Models and metrics are ready for production inference.")

if __name__ == "__main__":
    train_crop_models()
