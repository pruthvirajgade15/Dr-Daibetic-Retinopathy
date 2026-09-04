# 👁️ DR-Screening-AI: Clinical Deep Learning & Explainable AI Screening Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2%20(App%20Router)-black.svg)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, clinically grounded **Deep Learning, Computer Vision, and Explainable AI (XAI)** screening platform for automated **Diabetic Retinopathy (DR) grading**, automated Image Quality Assessment (IQA), anatomical attention localization, and clinical report generation.

> [!IMPORTANT]
> **Clinical AI Disclaimer:**  
> *“This system is an AI-assisted diagnostic screening tool and does not replace professional ophthalmic examination and clinical diagnosis by a licensed eye care specialist.”*

---

## 🌟 Key Features

- **🔬 5-Grade ICDR Classification:** Staging from **Grade 0 (No DR)** to **Grade 4 (Proliferative DR)** with confidence scoring.
- **🛡️ Automated Retinal Image Quality Assessment (IQA):** Real-time evaluation of Laplacian sharpness, SNR, illumination uniformity, and circular field-of-view gradability.
- **🧠 Explainable AI (XAI) with Grad-CAM:** Gradient-weighted Class Activation Mapping (Grad-CAM) overlaid with 5-zone anatomical quadrant energy distribution (Macula, Superior/Inferior Temporal, Superior/Inferior Nasal).
- **📋 Clinical Diagnostic Reports:** Automatically generates printable, EHR-ready A4 clinical screening reports with pathological biomarker audits (Microaneurysms, Exudates, Hemorrhages, Neovascularization).
- **📊 Interactive Next.js 14 Dashboard:** Modern medical UI with patient triage statistics, historical screening archive, interactive Grad-CAM opacity viewer, and direct PDF/print export.
- **🚀 Kaggle API Ingestion & Local ML Training:** Seamless dataset downloading via Kaggle API (`APTOS 2019`, `EyePACS`), customized EfficientNet-B0 transfer learning loop, and Quadratic Weighted Kappa (QWK) evaluation.

---

## 🏛️ Project Architecture & Directory Structure

```
DR-Screening-AI/
│
├── frontend/                              # Next.js 14 App Router + Tailwind CSS
│   ├── app/
│   │   ├── layout.tsx                     # Global layout & navigation shell
│   │   ├── page.tsx                       # Landing page & technology overview
│   │   ├── dashboard/
│   │   │   └── page.tsx                   # Clinical analytics & triage statistics
│   │   ├── screening/
│   │   │   └── page.tsx                   # Interactive upload & analysis studio
│   │   ├── results/
│   │   │   └── [id]/
│   │   │       └── page.tsx               # Dynamic patient diagnostic record & report
│   │   └── history/
│   │       └── page.tsx                   # Patient screening archive table
│   │
│   ├── components/
│   │   ├── Navbar.tsx                     # Navigation header
│   │   ├── ImageUploader.tsx              # Drag-and-drop fundus image uploader
│   │   ├── ImagePreview.tsx               # Retinal image & metadata preview
│   │   ├── QualityScore.tsx               # IQA focus, exposure & contrast gauges
│   │   ├── PredictionCard.tsx             # 5-Grade ICDR classification & referral card
│   │   ├── ConfidenceChart.tsx            # Softmax class probability breakdown
│   │   ├── GradCAMViewer.tsx              # Interactive Grad-CAM & structure viewer
│   │   ├── ScreeningReport.tsx            # XAI report card & print/PDF exporter
│   │   └── LoadingState.tsx               # Diagnostic analysis progress loader
│   │
│   ├── lib/
│   │   ├── api.ts                         # Native fetch API client wrapper
│   │   └── utils.ts                       # Grade colors & formatting utilities
│   │
│   ├── types/
│   │   └── screening.ts                   # TypeScript interfaces & types
│   │
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
│
├── backend/                               # FastAPI High-Performance Python Web API
│   ├── app/
│   │   ├── main.py                        # FastAPI application entrypoint
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── screening.py           # POST /api/screen (Image inference & XAI)
│   │   │   │   ├── health.py              # GET /api/health (System status)
│   │   │   │   └── history.py             # GET /api/history (Records & details)
│   │   │   └── dependencies.py            # DB session dependency injection
│   │   │
│   │   ├── core/
│   │   │   ├── config.py                  # Environment config & directory paths
│   │   │   └── security.py                # Session authentication helpers
│   │   │
│   │   ├── database/
│   │   │   ├── database.py                # SQLAlchemy engine & session factory
│   │   │   ├── models.py                  # ScreeningRecord ORM model
│   │   │   └── crud.py                    # Database query execution
│   │   │
│   │   ├── schemas/
│   │   │   ├── screening.py               # Pydantic request & response schemas
│   │   │   └── response.py                # Base response envelopes
│   │   │
│   │   ├── services/
│   │   │   ├── screening_service.py       # End-to-end pipeline orchestrator
│   │   │   ├── quality_service.py         # Image quality assessment wrapper
│   │   │   └── report_service.py          # Clinical HTML, PDF & TXT generator
│   │   │
│   │   ├── ml/
│   │   │   ├── model.py                   # PyTorch EfficientNet-B0 architecture
│   │   │   ├── preprocessing.py           # Ben Graham unsharp masking & CLAHE
│   │   │   ├── quality_assessment.py      # Laplacian focus & exposure IQA
│   │   │   ├── prediction.py              # 5-Grade ICDR inference engine
│   │   │   └── gradcam.py                 # Grad-CAM heatmaps & quadrant attention
│   │   │
│   │   └── utils/
│   │       ├── image_utils.py             # Base64 & NumPy conversions
│   │       └── file_utils.py              # File system storage persistence
│   │
│   ├── models/
│   │   └── efficientnet_dr.pth            # Active production PyTorch model weights
│   │
│   ├── tests/
│   │   ├── test_health.py                 # API health endpoint test
│   │   ├── test_prediction.py             # DL model forward pass & inference test
│   │   ├── test_quality.py                # Retinal focus & illumination IQA test
│   │   └── test_screening.py              # Full screening & history integration test
│   │
│   ├── requirements.txt                   # Backend dependencies
│   └── .env                               # Backend environment variables
│
│
├── database/
│   ├── schema.sql                         # SQLite / PostgreSQL DDL schema
│   └── migrations/                        # Database migration scripts
│
│
├── ml-training/                           # Model Development & ML Pipeline
│   ├── data/
│   │   ├── raw/                           # Downloaded dataset archives
│   │   ├── processed/                     # Preprocessed fundus images (3,600+ images)
│   │   └── metadata/                      # Sample manifests & CSV ground-truth labels
│   │
│   ├── notebooks/
│   │   └── experiments.ipynb              # Jupyter notebook exploration
│   │
│   ├── src/
│   │   ├── prepare_dataset.py             # Kaggle API downloader & dataset parser
│   │   ├── preprocessing.py               # Ben Graham CLAHE transformation
│   │   ├── train.py                       # PyTorch training loop with checkpointing
│   │   ├── evaluate.py                    # QWK, classification report & confusion matrix
│   │   └── explain.py                     # Batch Grad-CAM saliency extraction tool
│   │
│   └── outputs/
│       ├── checkpoints/                   # Saved checkpoints (best_dr_model.pth)
│       ├── metrics/                       # Evaluation JSONs & CSVs
│       └── plots/                         # Loss curves & confusion matrix plots
│
│
├── docs/
│   ├── architecture.md                    # System architecture & dataflow diagrams
│   ├── api.md                             # REST API specification
│   └── model.md                           # Deep Learning model architecture & metrics
│
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- *(Optional)* **Kaggle Account** for automated dataset downloads

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

### 3. Launch the Application

Run the backend and frontend in separate terminal windows:

#### Terminal 1: Backend (FastAPI on Port 8000)
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
- **API URL:** `http://localhost:8000`
- **Swagger Documentation:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/api/health`

#### Terminal 2: Frontend (Next.js 14 on Port 3000)
```powershell
cd frontend
npm run dev
```
- **Web Application:** `http://localhost:3000`

---

## 🤖 Machine Learning & Kaggle Training Pipeline

### 1. Download Datasets via Kaggle API
Ensure `~/.kaggle/kaggle.json` exists with your Kaggle API key:

```powershell
# Option A: Preprocessed Gaussian-Filtered Dataset (Recommended, 3,662 images)
python ml-training/src/prepare_dataset.py --kaggle_dataset sovitrath/diabetic-retinopathy-224x224-gaussian-filtered

# Option B: Full APTOS 2019 Dataset
python ml-training/src/prepare_dataset.py --kaggle_dataset mariaherrerot/aptos2019-blindness-detection
```

### 2. Train the Model Locally
```powershell
python ml-training/src/train.py --data_dir ml-training/data/processed --epochs 10 --batch_size 16 --lr 0.0001
```
> *Trained weights are automatically saved to `ml-training/outputs/checkpoints/best_dr_model.pth` and synced to `backend/models/efficientnet_dr.pth` for immediate web inference.*

### 3. Evaluate Model (QWK & Confusion Matrix)
```powershell
python ml-training/src/evaluate.py --weights backend/models/efficientnet_dr.pth --data_dir ml-training/data/processed
```

### 4. Batch Explainability Generation (Grad-CAM)
```powershell
python ml-training/src/explain.py --input_dir ml-training/data/processed --output_dir ml-training/outputs/plots --count 10
```

---

## 🔬 Explainable AI (XAI) & Report Generation

Every screening analysis produces a **Multi-Modal Diagnostic Report**:
1. **Original Fundus Image**: Raw RGB retinal input.
2. **Ben Graham Preprocessing**: Circular crop and local color contrast equalization.
3. **Grad-CAM Activation Map**: Gradient saliency highlighting lesions.
4. **Retinal Vascular & Disc Segmentation**: Landmark feature map.
5. **Quadrant Attribution Matrix**: Saliency distribution across Macula/Fovea, Temporal & Nasal arcades.
6. **Pathological Biomarker Checklist**: Microaneurysms, Hemorrhages, Hard/Soft Exudates, and Neovascularization detection rationale.

---

## 🧪 Automated Testing & Production Build Verification

```powershell
# Run Backend Test Suite (Pytest)
python -m pytest backend/tests -v

# Validate Next.js Production Build
cd frontend
npm run build
cd ..
```

---

## 🌐 Deployment Guidelines

### Option A: Docker Deployment
```bash
# Build and run containers
docker-compose up --build
```

### Option B: Cloud Hosting
- **Backend:** Deploy on **Render / Fly.io / AWS ECS / Google Cloud Run** using `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Frontend:** Deploy on **Vercel** with the root directory set to `frontend/` and environment variable `NEXT_PUBLIC_BACKEND_URL` pointing to your backend URL.

---

## 📄 License & Disclaimer

Distributed under the **MIT License**.

> **Medical Disclaimer:** This software is designed for research, academic, and clinical decision support purposes. It is not intended as a substitute for professional medical judgment, diagnosis, or treatment.
