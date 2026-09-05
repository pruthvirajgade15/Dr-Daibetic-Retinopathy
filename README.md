# 👁️ DR-Screening-AI: Clinical Deep Learning & Explainable AI Screening Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B%20(CUDA%20%2B%20AMP)-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2%20(App%20Router)-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Gradio](https://img.shields.io/badge/Gradio-Free%20Web%20App-FF7C00.svg?logo=gradio&logoColor=white)](https://gradio.app/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, human-centered **Deep Learning, Computer Vision, and Explainable AI (XAI)** clinical decision support platform for autonomous **Diabetic Retinopathy (DR) grading**, automated Image Quality Assessment (IQA), anatomical attention localization, and clinical report generation.

---

> [!IMPORTANT]
> ### 🩺 Clinical AI & Ethical Healthcare Disclaimer
> *“This platform is developed as an ophthalmological AI decision support and triage assistant. It is designed to assist healthcare professionals in early identification of vision-threatening pathology, but does **not** replace a comprehensive dilated clinical examination and final diagnosis by a licensed ophthalmologist or eye care specialist.”*

---

## 🌍 The Clinical Motivation: Why Early DR Screening Matters

**Diabetic Retinopathy (DR)** is the leading cause of preventable blindness among working-age adults worldwide, affecting more than **100 million individuals** living with diabetes. 

- **The Problem:** In its early stages, diabetic retinopathy progresses silently with **zero symptoms**. By the time patients notice vision degradation, permanent microvascular retinal damage has often occurred.
- **The Challenge:** Periodic dilated retinal exams are inaccessible in underserved clinics and rural communities due to severe shortages of trained ophthalmologists and retinal specialists.
- **Our Solution:** **DR-Screening-AI** bridges this critical gap by providing an automated, transparent, multi-modal screening pipeline that assesses retinal image gradability, identifies early-stage microvascular lesions, generates visual Grad-CAM activation maps, and triages patients based on clinical urgency.

---

## ✨ Core Clinical & Engineering Capabilities

| Feature | Clinical & Technical Description |
| :--- | :--- |
| **🔬 5-Grade ICDR Staging** | Multi-class Softmax classification following the **International Clinical Diabetic Retinopathy (ICDR)** standard: *Grade 0 (No DR)* $\rightarrow$ *Grade 1 (Mild)* $\rightarrow$ *Grade 2 (Moderate)* $\rightarrow$ *Grade 3 (Severe)* $\rightarrow$ *Grade 4 (Proliferative DR)*. |
| **🛡️ Automated Image Quality (IQA)** | Laplacian focus variance, signal-to-noise ratio (SNR), exposure uniformity, and circular field-of-view masking to prevent misdiagnosis on blurry or ungradable scans. |
| **🧠 Explainable AI (XAI) & Grad-CAM** | Computes gradient-weighted class activation mapping (Grad-CAM) overlaid directly on retinal fundus scans to highlight microaneurysms, hemorrhages, and lipid exudates. |
| **📍 5-Zone Retinal Quadrant Saliency** | Energy attribution breakdown across the **Central Macula & Fovea**, **Superior Temporal Arcade**, **Inferior Temporal Arcade**, **Superior Nasal**, and **Inferior Nasal** zones. |
| **📋 Automated Clinical Screening Reports** | One-click generation of printable **A4 Clinical Reports** formatted for Electronic Health Record (EHR) integration and clinical referral documentation. |
| **⚡ GPU Accelerated (CUDA & AMP)** | PyTorch training and inference optimized with **Automatic Mixed Precision (FP16)** for fast, low-latency execution on NVIDIA GPUs (e.g., RTX 4060). |
| **🎨 Multi-Frontend Ecosystem** | Choice of a modern **Next.js 14 Web Studio** with patient intake forms or a **100% Free Gradio Web Demo** ready for one-click deployment. |

---

## 🔬 Multi-Modal Visual Diagnostics Pipeline

Every retinal scan passes through a synchronized 4-panel computer vision pipeline:

```
 ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
 │  1. Original Fundus  │ ──> │  2. Ben Graham CLAHE │ ──> │  3. Grad-CAM Saliency│ ──> │  4. Retinal Vessels  │
 │  Raw clinical input  │     │ Contrast enhancement │     │  Pathology heatmap   │     │ & Optic Disc segment │
 └──────────────────────┘     └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

1. **Original Retinal Fundus:** Raw RGB fundus photograph from digital fundus cameras.
2. **Ben Graham + CLAHE:** Circular field-of-view boundary crop and Contrast Limited Adaptive Histogram Equalization to neutralize illumination variability.
3. **Grad-CAM Saliency Map:** Gradient activations from EfficientNet-B0 feature blocks revealing exact lesion coordinates.
4. **Vascular & Landmark Segmentation:** Structural extraction of the retinal vessel tree and optic nerve disc.

---

## 🏛️ System Architecture & Project Structure

```
DR-Screening-AI/
│
├── frontend/                              # Next.js 14 App Router + Tailwind CSS
│   ├── app/
│   │   ├── layout.tsx                     # Global clinical theme & navbar shell
│   │   ├── page.tsx                       # Interactive landing page & capabilities
│   │   ├── dashboard/
│   │   │   └── page.tsx                   # Clinical triage statistics & telemetry
│   │   ├── screening/
│   │   │   └── page.tsx                   # Interactive upload, analysis & XAI studio
│   │   ├── results/[id]/
│   │   │   └── page.tsx                   # Dynamic patient diagnostic record & report
│   │   └── history/
│   │       └── page.tsx                   # Patient screening archive table
│   │
│   ├── components/                        # Modular React medical UI components
│   │   ├── Navbar.tsx                     # Top navigation bar
│   │   ├── ImageUploader.tsx              # Drag-and-drop fundus image dropzone
│   │   ├── ImagePreview.tsx               # Retinal image & patient metadata card
│   │   ├── QualityScore.tsx               # Focus, illumination & contrast gauges
│   │   ├── PredictionCard.tsx             # 5-Grade ICDR classification card
│   │   ├── ConfidenceChart.tsx            # Softmax class probability bars
│   │   ├── GradCAMViewer.tsx              # Multi-modal Grad-CAM & opacity viewer
│   │   ├── ScreeningReport.tsx            # XAI report card & print/PDF exporter
│   │   └── LoadingState.tsx               # Medical diagnostic animation loader
│   │
│   ├── lib/                               # API clients & formatting utilities
│   └── types/                             # TypeScript interfaces & medical types
│
│
├── backend/                               # High-Performance FastAPI Python API
│   ├── app/
│   │   ├── main.py                        # FastAPI application entrypoint
│   │   ├── api/routes/                    # /api/screen, /api/health, /api/history
│   │   ├── core/                          # Settings, security & directory config
│   │   ├── database/                      # SQLAlchemy ORM models & SQLite/Postgres CRUD
│   │   ├── ml/                            # PyTorch EfficientNet-B0, IQA, CLAHE, Grad-CAM
│   │   ├── schemas/                       # Pydantic validation schemas
│   │   └── services/                      # Screening orchestration & report generation
│   │
│   ├── models/
│   │   └── efficientnet_dr.pth            # Active production PyTorch model weights
│   ├── tests/                             # Pytest test suite (6/6 passing)
│   ├── Dockerfile                         # Container configuration
│   └── requirements.txt                   # Backend dependencies
│
│
├── ml-training/                           # Machine Learning Training Pipeline
│   ├── data/                              # Processed fundus images (3,662+ samples)
│   ├── notebooks/experiments.ipynb        # Exploratory data analysis & experiments
│   ├── src/
│   │   ├── prepare_dataset.py             # Kaggle API downloader & dataset parser
│   │   ├── preprocessing.py               # Ben Graham CLAHE dataset transforms
│   │   ├── train.py                       # PyTorch GPU training loop (AMP + Tensor Cores)
│   │   ├── evaluate.py                    # QWK, classification report & confusion matrix
│   │   └── explain.py                     # Batch Grad-CAM saliency generator
│   └── outputs/                           # Checkpoints, evaluation metrics & plots
│
│
├── database/                              # SQL schemas & migration scripts
├── docs/                                  # System architecture, API & deployment guides
├── gradio_app.py                          # Standalone 100% Free Gradio Web Application
├── requirements.txt                       # Python dependencies
├── README.md                              # Comprehensive documentation
└── .gitignore                             # Clean version control configuration
```

---

## ⚡ Quick Start: Running Locally in 2 Minutes

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- *(Optional)* **NVIDIA GPU** with CUDA support for accelerated training

### 2. Install Dependencies

```powershell
# Install Backend & ML Dependencies
pip install -r backend/requirements.txt

# Install Frontend Dependencies
cd frontend
npm install
cd ..
```

---

### 3. Launch the Full-Stack Application

Open two separate PowerShell terminal windows:

#### Terminal 1 — Start the FastAPI Backend
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Endpoint:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

#### Terminal 2 — Start the Next.js Frontend
```powershell
cd frontend
npm run dev
```
- **Frontend Web Studio:** [http://localhost:3000](http://localhost:3000)
- **Screening Studio:** [http://localhost:3000/screening](http://localhost:3000/screening)

---

### 🎨 (Alternative) Launch the Free Standalone Gradio App
If you want to run the lightweight, single-file interactive demo:
```powershell
python gradio_app.py
```
- **Gradio Web App:** [http://localhost:7860](http://localhost:7860)

---

## 🤖 Deep Learning & Kaggle Training Pipeline

### 1. Download Datasets via Kaggle API
Ensure `~/.kaggle/kaggle.json` exists with your Kaggle API key:

```powershell
# Download 3,662 preprocessed 224x224 Gaussian filtered images (APTOS 2019)
python ml-training/src/prepare_dataset.py --kaggle_dataset sovitrath/diabetic-retinopathy-224x224-gaussian-filtered
```

### 2. High-Performance GPU Training (NVIDIA RTX 4060 / CUDA)
Our training script leverages **Automatic Mixed Precision (FP16)** and **Tensor Cores**:

```powershell
# Train EfficientNet-B0 with batch size 32 for 15 epochs
python ml-training/src/train.py --data_dir ml-training/data/processed --epochs 15 --batch_size 32 --lr 0.0001
```
> *Trained weights are automatically saved to `ml-training/outputs/checkpoints/best_dr_model.pth` and synced to `backend/models/efficientnet_dr.pth` for immediate live web inference.*

### 3. Evaluate Model (Quadratic Weighted Kappa & Confusion Matrix)
```powershell
python ml-training/src/evaluate.py --weights backend/models/efficientnet_dr.pth --data_dir ml-training/data/processed
```

### 4. Generate Batch Grad-CAM Saliency Plots
```powershell
python ml-training/src/explain.py --input_dir ml-training/data/processed --output_dir ml-training/outputs/plots --count 10
```

---

## 🌐 100% Free Production Deployment Guide

### Option 1: Free 24/7 Hosting on Hugging Face Spaces (Gradio)

Hugging Face provides **unlimited, 100% free hosting** for Gradio applications.

1. Create a free space at **[https://huggingface.co/new-space](https://huggingface.co/new-space)**:
   - **Space Name:** `dr-screening-ai`
   - **SDK:** `Gradio`
   - **Hardware:** `CPU Basic - Free`
   - **Visibility:** `Public`
2. Push the files to your space:
   ```powershell
   cd d:\GitHub
   git clone https://huggingface.co/spaces/pruthvirajgade15/dr-screening-ai free-hf-space
   Copy-Item -Path "Dr-Daibetic-Retinopathy\gradio_app.py" -Destination "free-hf-space\app.py"
   Copy-Item -Path "Dr-Daibetic-Retinopathy\requirements.txt" -Destination "free-hf-space\requirements.txt"
   Copy-Item -Path "Dr-Daibetic-Retinopathy\backend" -Destination "free-hf-space\backend" -Recurse -Force
   Copy-Item -Path "Dr-Daibetic-Retinopathy\ml-training\data\processed" -Destination "free-hf-space\ml-training\data\processed" -Recurse -Force
   cd free-hf-space
   git add .
   git commit -m "feat: deploy free Gradio DR screening app"
   git push
   ```
3. Your app is live at: `https://huggingface.co/spaces/pruthvirajgade15/dr-screening-ai`

---

### Option 2: Full-Stack Vercel + Hugging Face API

- **Backend:** Deploy `backend/` to a Hugging Face **Docker Space** $\rightarrow$ `https://<user>-dr-screening-backend.hf.space`.
- **Frontend:** Deploy `frontend/` to **Vercel** with environment variable `NEXT_PUBLIC_BACKEND_URL=https://<user>-dr-screening-backend.hf.space`.
*(Detailed walkthrough available in [`docs/deployment.md`](file:///d:/GitHub/Dr-Daibetic-Retinopathy/docs/deployment.md)).*

---

## 🧪 Automated Testing & Verification

Every component is covered by comprehensive unit and integration tests:

```powershell
# Run Backend Test Suite (Pytest)
python -m pytest backend/tests -v

# Validate Next.js 14 Production Build
cd frontend
npm run build
cd ..
```

**Test Verification Status:**
- ✅ `test_health_check`: API health & readiness
- ✅ `test_model_instantiation`: PyTorch EfficientNet-B0 architecture validation
- ✅ `test_prediction_output`: 5-Grade ICDR Softmax staging
- ✅ `test_assess_quality`: Laplacian focus & illumination IQA
- ✅ `test_screen_flow`: End-to-end multi-modal screening pipeline
- ✅ `test_history_flow`: SQLite database patient history CRUD
- ✅ `Next.js Production Build`: 0 errors across all static and dynamic routes

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for more information.

Developed with ❤️ for advancing accessible, transparent, and clinically grounded artificial intelligence in healthcare.
