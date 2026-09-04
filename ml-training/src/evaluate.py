import os
import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import cohen_kappa_score, classification_report, confusion_matrix
from torchvision import models
import torch.nn as nn

from train import RetinalDataset

def evaluate_model(
    weights_path: str = "backend/models/efficientnet_dr.pth",
    data_dir: str = "ml-training/data/processed",
    csv_path: str = "ml-training/data/metadata/sample_manifest.csv"
):
    ds = RetinalDataset(data_dir, csv_path if os.path.exists(csv_path) else None)
    if len(ds) == 0:
        print(f"[!] No dataset samples found in {data_dir} to evaluate.")
        return

    loader = DataLoader(ds, batch_size=8, shuffle=False)
    
    model = models.efficientnet_b0()
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Linear(in_features, 512),
        nn.LayerNorm(512),
        nn.SiLU(),
        nn.Dropout(0.3),
        nn.Linear(512, 128),
        nn.LayerNorm(128),
        nn.SiLU(),
        nn.Linear(128, 5)
    )

    if os.path.exists(weights_path):
        ckpt = torch.load(weights_path, map_location="cpu")
        model.load_state_dict(ckpt.get("model_state_dict", ckpt))
        print(f"[+] Loaded weights from {weights_path}")
    else:
        print(f"[!] Model weights not found at {weights_path}, evaluating uninitialized weights.")

    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for imgs, labels in loader:
            outputs = model(imgs)
            preds = outputs.argmax(dim=-1).numpy()
            y_true.extend(labels.numpy())
            y_pred.extend(preds)

    qwk = cohen_kappa_score(y_true, y_pred, weights="quadratic")
    cm = confusion_matrix(y_true, y_pred)
    print("\n--- MODEL EVALUATION ---")
    print(f"Quadratic Weighted Kappa (QWK): {qwk:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))
    print("Confusion Matrix:")
    print(cm)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate Diabetic Retinopathy Model")
    parser.add_argument("--weights", type=str, default="backend/models/efficientnet_dr.pth", help="Path to model weights")
    parser.add_argument("--data_dir", type=str, default="ml-training/data/processed", help="Path to processed image directory")
    parser.add_argument("--csv_path", type=str, default="ml-training/data/metadata/sample_manifest.csv", help="Path to CSV labels")
    args = parser.parse_args()

    evaluate_model(weights_path=args.weights, data_dir=args.data_dir, csv_path=args.csv_path)
