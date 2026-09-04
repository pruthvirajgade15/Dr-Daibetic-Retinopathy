import os
import sys
import argparse
import zipfile
import shutil
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw

def download_from_kaggle(
    dataset_slug: str = "sovitrath/diabetic-retinopathy-224x224-gaussian-filtered",
    is_competition: bool = False,
    target_raw_dir: str = "ml-training/data/raw",
    target_processed_dir: str = "ml-training/data/processed",
    metadata_dir: str = "ml-training/data/metadata"
):
    """
    Downloads and extracts a Diabetic Retinopathy dataset from Kaggle.
    """
    os.makedirs(target_raw_dir, exist_ok=True)
    os.makedirs(target_processed_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        print(f"[+] Kaggle API Authenticated successfully.")
    except Exception as e:
        print(f"[!] Error authenticating with Kaggle API: {e}")
        print("    Please ensure ~/.kaggle/kaggle.json exists with valid credentials.")
        return False

    print(f"[*] Downloading '{dataset_slug}' to {target_raw_dir}...")
    try:
        if is_competition:
            api.competition_download_files(dataset_slug, path=target_raw_dir, quiet=False)
        else:
            api.dataset_download_files(dataset_slug, path=target_raw_dir, unzip=False, quiet=False)
        print("[+] Download complete!")
    except Exception as e:
        print(f"[!] Download failed: {e}")
        return False

    # Extract any zip files in raw directory
    print(f"[*] Extracting archives to {target_processed_dir}...")
    for item in os.listdir(target_raw_dir):
        if item.endswith(".zip"):
            zip_path = os.path.join(target_raw_dir, item)
            print(f"    Extracting {item}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_processed_dir)

    # Search for CSV labels
    csv_found = None
    for root, _, files in os.walk(target_processed_dir):
        for f in files:
            if f.endswith(".csv") and ("train" in f.lower() or "manifest" in f.lower() or "labels" in f.lower()):
                csv_found = os.path.join(root, f)
                break
        if csv_found:
            break

    if csv_found:
        dest_csv = os.path.join(metadata_dir, "sample_manifest.csv")
        shutil.copy(csv_found, dest_csv)
        df = pd.read_csv(dest_csv)
        print(f"[+] Found labels metadata: {dest_csv} ({len(df)} records)")
    else:
        # Build manifest from subfolders (e.g. 0_No_DR, 1_Mild, etc.)
        manifest_rows = []
        for root, _, files in os.walk(target_processed_dir):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    label = 0
                    for grade, gname in enumerate(["no_dr", "mild", "moderate", "severe", "proliferative"]):
                        if gname in f.lower() or gname in root.lower() or f"{grade}" in root.lower():
                            label = grade
                            break
                    manifest_rows.append({
                        "id_code": os.path.splitext(f)[0],
                        "diagnosis": label,
                        "file_path": os.path.join(root, f)
                    })
        if manifest_rows:
            dest_csv = os.path.join(metadata_dir, "sample_manifest.csv")
            pd.DataFrame(manifest_rows).to_csv(dest_csv, index=False)
            print(f"[+] Generated manifest index with {len(manifest_rows)} images at: {dest_csv}")

    print(f"\n[+] Dataset ready for training in: {target_processed_dir}")
    return True

def generate_synthetic_fundus_dataset(output_dir: str = "ml-training/data/processed", num_per_class: int = 4):
    """
    Generates synthetic high-resolution retinal fundus images for all 5 DR classes.
    """
    os.makedirs(output_dir, exist_ok=True)
    classes = [
        (0, "No_DR"),
        (1, "Mild_DR"),
        (2, "Moderate_DR"),
        (3, "Severe_DR"),
        (4, "Proliferative_DR"),
    ]

    manifest_rows = []
    width, height = 512, 512

    for grade, class_name in classes:
        for idx in range(1, num_per_class + 1):
            file_name = f"fundus_{class_name}_{idx:03d}.png"
            file_path = os.path.join(output_dir, file_name)

            img = Image.new("RGB", (width, height), (8, 5, 5))
            draw = ImageDraw.Draw(img)

            # Draw fundus sphere
            draw.ellipse([20, 20, width - 20, height - 20], fill=(160, 50, 25), outline=(90, 20, 10))
            od_x, od_y = 380, 256
            draw.ellipse([od_x - 35, od_y - 35, od_x + 35, od_y + 35], fill=(245, 200, 120))
            draw.ellipse([220, 240, 280, 280], fill=(110, 30, 15))

            if grade >= 1:
                for _ in range(8 * grade):
                    rx, ry = np.random.randint(100, 400), np.random.randint(100, 400)
                    draw.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=(80, 0, 0))
            if grade >= 2:
                for _ in range(6 * grade):
                    rx, ry = np.random.randint(120, 380), np.random.randint(120, 380)
                    draw.ellipse([rx - 5, ry - 5, rx + 5, ry + 5], fill=(230, 220, 140))
            if grade >= 3:
                for _ in range(4 * grade):
                    rx, ry = np.random.randint(130, 360), np.random.randint(130, 360)
                    draw.ellipse([rx - 8, ry - 8, rx + 8, ry + 8], fill=(210, 210, 200))
            if grade >= 4:
                for _ in range(12):
                    rx, ry = np.random.randint(150, 350), np.random.randint(150, 350)
                    draw.line([rx, ry, rx + np.random.randint(-20, 20), ry + np.random.randint(-20, 20)], fill=(120, 0, 0), width=3)

            img.save(file_path)
            manifest_rows.append({
                "id_code": file_name.replace(".png", ""),
                "diagnosis": grade,
                "stage": class_name.replace("_", " "),
                "file_path": file_path
            })

    meta_dir = "ml-training/data/metadata"
    os.makedirs(meta_dir, exist_ok=True)
    manifest_csv = os.path.join(meta_dir, "sample_manifest.csv")
    df = pd.DataFrame(manifest_rows)
    df.to_csv(manifest_csv, index=False)
    print(f"[+] Prepared synthetic dataset with {len(manifest_rows)} samples at: {manifest_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare Diabetic Retinopathy Dataset")
    parser.add_argument("--kaggle_dataset", type=str, default="", help="Kaggle dataset slug (e.g. sovitrath/diabetic-retinopathy-224x224-gaussian-filtered)")
    parser.add_argument("--kaggle_competition", type=str, default="", help="Kaggle competition slug (e.g. aptos2019-blindness-detection)")
    parser.add_argument("--synthetic", action="store_true", help="Generate synthetic fundus images locally")
    parser.add_argument("--num_samples", type=int, default=4, help="Samples per class for synthetic generation")
    args = parser.parse_args()

    if args.kaggle_dataset:
        download_from_kaggle(args.kaggle_dataset, is_competition=False)
    elif args.kaggle_competition:
        download_from_kaggle(args.kaggle_competition, is_competition=True)
    else:
        # Default: download popular preprocessed dataset or generate synthetic
        if not args.synthetic:
            print("[*] No specific Kaggle slug provided. Downloading default preprocessed dataset: 'sovitrath/diabetic-retinopathy-224x224-gaussian-filtered'...")
            success = download_from_kaggle("sovitrath/diabetic-retinopathy-224x224-gaussian-filtered", is_competition=False)
            if not success:
                print("[*] Falling back to local synthetic generation...")
                generate_synthetic_fundus_dataset(num_per_class=args.num_samples)
        else:
            generate_synthetic_fundus_dataset(num_per_class=args.num_samples)
