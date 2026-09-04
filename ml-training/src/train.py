import os
import sys
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import models
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.metrics import cohen_kappa_score

from preprocessing import ben_graham_clahe

class RetinalDataset(Dataset):
    def __init__(self, data_dir: str, csv_path: str = None, image_size: int = 224):
        self.data_dir = data_dir
        self.image_size = image_size
        self.samples = []
        
        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            id_col = 'id_code' if 'id_code' in df.columns else df.columns[0]
            label_col = 'diagnosis' if 'diagnosis' in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
            
            for _, row in df.iterrows():
                fname = str(row[id_col])
                if not fname.endswith(('.png', '.jpg', '.jpeg')):
                    fname = f"{fname}.png"
                fpath = row.get("file_path", os.path.join(data_dir, fname))
                if os.path.exists(fpath):
                    self.samples.append((fpath, int(row[label_col]) if label_col else 0))
                else:
                    # Search recursively for the image
                    for root, _, files in os.walk(data_dir):
                        if fname in files or f"{row[id_col]}.png" in files or f"{row[id_col]}.jpg" in files:
                            self.samples.append((os.path.join(root, fname), int(row[label_col]) if label_col else 0))
                            break
        else:
            for root, _, files in os.walk(data_dir):
                for f in files:
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                        grade = 0
                        for i, gname in enumerate(["no_dr", "mild", "moderate", "severe", "proliferative"]):
                            if gname in f.lower() or gname in root.lower() or f"{i}" in root.lower():
                                grade = i
                                break
                        self.samples.append((os.path.join(root, f), grade))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        fpath, label = self.samples[idx]
        img = np.array(Image.open(fpath).convert("RGB"))
        prep = ben_graham_clahe(img, image_size=self.image_size)
        norm = (prep.astype(np.float32) / 255.0 - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
        tensor = torch.tensor(norm.transpose(2, 0, 1), dtype=torch.float32)
        return tensor, label

def train_model(
    data_dir: str = "ml-training/data/processed",
    csv_path: str = "ml-training/data/metadata/sample_manifest.csv",
    epochs: int = 15,
    batch_size: int = 8,
    lr: float = 1e-4
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training on device: {device}")
    
    ds = RetinalDataset(data_dir, csv_path if os.path.exists(csv_path) else None)
    if len(ds) == 0:
        print(f"[!] No dataset samples found in {data_dir}. Run prepare_dataset.py first.")
        return

    print(f"[*] Found {len(ds)} training images.")
    loader = DataLoader(ds, batch_size=min(batch_size, len(ds)), shuffle=True)
    
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
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
    model.to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    best_loss = float("inf")
    os.makedirs("ml-training/outputs/checkpoints", exist_ok=True)
    os.makedirs("backend/models", exist_ok=True)

    print(f"[*] Starting PyTorch EfficientNet-B0 training for {epochs} epochs...")
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(loader)
        print(f"Epoch [{epoch:02d}/{epochs:02d}] Loss: {avg_loss:.4f}")

        if avg_loss < best_loss:
            best_loss = avg_loss
            ckpt_path = "ml-training/outputs/checkpoints/best_dr_model.pth"
            backend_model_path = "backend/models/efficientnet_dr.pth"
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "loss": best_loss
            }, ckpt_path)
            torch.save(model.state_dict(), backend_model_path)
            print(f"  [+] Saved best model -> {ckpt_path} & {backend_model_path}")

    print(f"\n[+] Training Complete! Best Loss: {best_loss:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Diabetic Retinopathy Model")
    parser.add_argument("--data_dir", type=str, default="ml-training/data/processed", help="Path to image directory")
    parser.add_argument("--csv_path", type=str, default="ml-training/data/metadata/sample_manifest.csv", help="Path to CSV labels")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    args = parser.parse_args()

    train_model(
        data_dir=args.data_dir,
        csv_path=args.csv_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr
    )
