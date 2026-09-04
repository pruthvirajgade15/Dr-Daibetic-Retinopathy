# System Architecture

## Overview
DR-Screening-AI is a tele-ophthalmology clinical decision-support system for automated Diabetic Retinopathy (DR) grading and Explainable AI (XAI) lesion visualization.

## High-Level Architecture

```
+-------------------------------------------------------------------+
|                  Frontend (Next.js + Tailwind CSS)                |
|  - Landing Page     - Screening Studio      - Multi-Modal Viewer  |
|  - IQA Gauges       - Diagnostic Cards      - PDF/HTML Reports    |
+---------------------------------+---------------------------------+
                                  | HTTP / JSON & Multipart
                                  v
+---------------------------------+---------------------------------+
|                      Backend (FastAPI REST API)                   |
|  - /api/health      - /api/screen           - /api/history        |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                       Core ML & CV Pipeline                       |
|  1. Image Quality Assessment (IQA: Focus, Exposure, Contrast)     |
|  2. Ben Graham Preprocessing (Circular FOV + Gaussian Subtraction)|
|  3. PyTorch EfficientNet-B0 5-Grade ICDR Classification           |
|  4. Grad-CAM Lesion Heatmap & Anatomical Quadrant Saliency        |
|  5. Vascular Tree & Optic Disc Structural Segmentation            |
+-------------------------------------------------------------------+
```
