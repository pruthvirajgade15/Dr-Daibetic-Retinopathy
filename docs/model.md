# Deep Learning & Computer Vision Model Specification

## 1. Backbone Architecture
- **Base Architecture:** `EfficientNet-B0` (ImageNet transfer learning)
- **Modified Classification Head:**
  - `Linear(in_features, 512)` -> `LayerNorm(512)` -> `SiLU()` -> `Dropout(0.3)`
  - `Linear(512, 128)` -> `LayerNorm(128)` -> `SiLU()` -> `Dropout(0.15)`
  - `Linear(128, 5)` (Softmax multi-class)

## 2. 5-Grade ICDR Diabetic Retinopathy Scale
| Grade | Stage | Key Pathologies | Referral Action |
|---|---|---|---|
| **0** | **No DR** | None | Routine Annual Check |
| **1** | **Mild NPDR** | Microaneurysms | 6–9 Month Follow-up |
| **2** | **Moderate NPDR** | Hemorrhages, Hard Exudates | Specialist within 2–3 Months |
| **3** | **Severe NPDR** | >20 Intraretinal Hemorrhages in 4 Quadrants | Urgent Referral (2–4 Weeks) |
| **4** | **Proliferative DR** | Neovascularization, Vitreous Hemorrhage | Emergency Intervention (24–48 Hours) |

## 3. Explainability (XAI)
- **Grad-CAM Layer:** Last convolutional feature block (`features[-1]`).
- **Quadrant Saliency:** Real-time energy integration across Central Macula/Fovea, Superior/Inferior Temporal, and Superior/Inferior Nasal retinal zones.
