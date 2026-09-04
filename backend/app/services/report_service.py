import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from PIL import Image
from ..core.config import settings

class ReportService:
    @staticmethod
    def generate_report(
        screening_id: str,
        patient_id: str,
        eye: str,
        prediction: dict,
        quality: dict,
        explainability: dict,
        images_dict: dict
    ) -> Dict[str, str]:
        reports_dir = settings.REPORTS_DIR
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"DR_XAI_Report_{patient_id}_{eye}_{timestamp}"

        # Save individual images for clinical archive
        orig_file = reports_dir / f"{base_name}_orig.png"
        prep_file = reports_dir / f"{base_name}_prep.png"
        grad_file = reports_dir / f"{base_name}_grad.png"
        struct_file = reports_dir / f"{base_name}_struct.png"

        Image.fromarray(images_dict["original"]).save(orig_file)
        Image.fromarray(images_dict["preprocessed"]).save(prep_file)
        Image.fromarray(images_dict["gradcam"]).save(grad_file)
        Image.fromarray(images_dict["structures"]).save(struct_file)

        grade_colors = {
            0: "#10b981", 1: "#06b6d4", 2: "#f59e0b", 3: "#f97316", 4: "#ef4444"
        }
        color = grade_colors.get(prediction.get("grade", 0), "#3b82f6")
        quadrants = explainability.get("quadrants", {})
        lesions = explainability.get("lesion_signatures", {})

        quadrant_rows = "".join([
            f"<tr><td style='padding:8px 12px; border-bottom:1px solid #334155;'>{k.replace('_', ' ').title()}</td>"
            f"<td style='padding:8px 12px; border-bottom:1px solid #334155; font-weight:bold; text-align:right;'>{v}%</td>"
            f"<td style='padding:8px 12px; border-bottom:1px solid #334155;'><div style='background:#334155; border-radius:4px; overflow:hidden; height:8px;'><div style='background:#06b6d4; height:100%; width:{min(100, v*2)}%;'></div></div></td></tr>"
            for k, v in quadrants.items()
        ])

        lesion_rows = "".join([
            f"<tr><td style='padding:8px 12px; border-bottom:1px solid #334155; font-weight:600;'>{k.replace('_', ' ').title()}</td>"
            f"<td style='padding:8px 12px; border-bottom:1px solid #334155; color:{'#f87171' if 'Detected' in v or 'present' in v or 'infarcts' in v or 'visible' in v else '#94a3b8'};'>{v}</td></tr>"
            for k, v in lesions.items()
        ])

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Explainable AI Clinical Report - {patient_id}</title>
    <style>
        @media print {{
            body {{ background: #ffffff !important; color: #000000 !important; padding: 0 !important; }}
            .card {{ border: none !important; box-shadow: none !important; background: #ffffff !important; color: #000000 !important; max-width: 100% !important; }}
            .no-print {{ display: none !important; }}
            .img-card {{ border: 1px solid #cccccc !important; background: #f8fafc !important; }}
            .disclaimer {{ background: #fef3c7 !important; color: #92400e !important; border-left: 4px solid #d97706 !important; }}
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #090d16; color: #f8fafc; padding: 32px 16px; margin: 0; line-height: 1.5; }}
        .card {{ background: #131b2e; border-radius: 16px; padding: 32px; border: 1px solid #1e293b; max-width: 960px; margin: 0 auto; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
        .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #1e293b; padding-bottom: 20px; margin-bottom: 24px; }}
        .badge {{ background: {color}; color: #ffffff; padding: 6px 18px; border-radius: 9999px; font-weight: 800; font-size: 15px; letter-spacing: 0.5px; }}
        .badge-sub {{ background: #1e293b; color: #38bdf8; border: 1px solid #0284c7; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: #38bdf8; border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin: 28px 0 16px 0; text-transform: uppercase; letter-spacing: 1px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 16px 0; }}
        .info-box {{ background: #0b1120; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; }}
        .info-row {{ display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px; border-bottom: 1px solid #1e293b; }}
        .info-row:last-child {{ border-bottom: none; }}
        .img-card {{ background: #0b1120; border-radius: 10px; padding: 10px; text-align: center; border: 1px solid #1e293b; }}
        .img-card img {{ width: 100%; border-radius: 6px; aspect-ratio: 1/1; object-fit: cover; }}
        .img-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin: 6px 0 0 0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        .disclaimer {{ background: #451a03; border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin-top: 32px; font-size: 12px; color: #fde68a; }}
        .print-btn {{ background: #06b6d4; color: #020617; padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; border: none; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="no-print" style="text-align: right; margin-bottom: 16px;">
            <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
        </div>

        <div class="header">
            <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                    <span class="badge-sub">Explainable AI (XAI)</span>
                    <span class="badge-sub">Autonomous Screening</span>
                </div>
                <h1 style="margin:0; font-size:24px; font-weight:800; color:#ffffff;">Diabetic Retinopathy Clinical Saliency Report</h1>
                <p style="margin:4px 0 0 0; color:#94a3b8; font-size:12px;">Screening Reference: {screening_id} | Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <div style="text-align:right;">
                <div class="badge">{prediction.get('stage', 'Unknown')}</div>
                <div style="font-size:12px; color:#94a3b8; margin-top:6px;">Confidence: <b>{prediction.get('confidence', 0)}%</b></div>
            </div>
        </div>

        <div class="grid-2">
            <div class="info-box">
                <div style="font-weight:700; color:#38bdf8; font-size:13px; margin-bottom:8px;">PATIENT & EXAM SPECIFICATION</div>
                <div class="info-row"><span>Patient Identifier:</span><b>{patient_id}</b></div>
                <div class="info-row"><span>Examined Eye:</span><b>{eye}</b></div>
                <div class="info-row"><span>Referable DR:</span><b style="color:{'#ef4444' if prediction.get('is_referable') else '#10b981'};">{'Yes (Referral Required)' if prediction.get('is_referable') else 'No (Routine Annual)'}</b></div>
                <div class="info-row"><span>Clinical Urgency:</span><b>{prediction.get('clinical_urgency', 'Routine')}</b></div>
            </div>

            <div class="info-box">
                <div style="font-weight:700; color:#38bdf8; font-size:13px; margin-bottom:8px;">IMAGE QUALITY AUDIT</div>
                <div class="info-row"><span>Overall Quality:</span><b>{quality.get('status', 'Acceptable')} ({quality.get('overall_quality_score', 0)}/100)</b></div>
                <div class="info-row"><span>Clarity / Sharpness:</span><b>{quality.get('sharpness_score', 0)}/100</b></div>
                <div class="info-row"><span>Uniform Illumination:</span><b>{quality.get('illumination_score', 0)}/100</b></div>
                <div class="info-row"><span>Optic Disc Visibility:</span><b>{quality.get('disc_detected', 'Visible')}</b></div>
            </div>
        </div>

        <div class="section-title">Multi-Modal Computer Vision Diagnostics</div>
        <div class="grid-4">
            <div class="img-card"><img src="{orig_file.name}"><p class="img-label">1. Original Fundus</p></div>
            <div class="img-card"><img src="{prep_file.name}"><p class="img-label">2. Ben Graham CLAHE</p></div>
            <div class="img-card"><img src="{grad_file.name}"><p class="img-label">3. Grad-CAM Saliency</p></div>
            <div class="img-card"><img src="{struct_file.name}"><p class="img-label">4. Vessels & Landmarks</p></div>
        </div>

        <div class="section-title">Explainable AI (XAI) Saliency & Attention Analysis</div>
        <div class="grid-2">
            <div class="info-box">
                <div style="font-weight:700; color:#38bdf8; font-size:13px; margin-bottom:8px;">ANATOMICAL QUADRANT ATTRIBUTION</div>
                <table>
                    <thead>
                        <tr style="color:#94a3b8; text-align:left; font-size:11px; text-transform:uppercase;">
                            <th style="padding:6px 12px;">Quadrant</th>
                            <th style="padding:6px 12px; text-align:right;">Attention</th>
                            <th style="padding:6px 12px; width:40%;">Visual Distribution</th>
                        </tr>
                    </thead>
                    <tbody>
                        {quadrant_rows}
                    </tbody>
                </table>
                <p style="font-size:12px; color:#94a3b8; margin-top:10px;">Primary Activation Focus: <b style="color:#38bdf8;">{explainability.get('dominant_quadrant', 'Central Macula')}</b></p>
            </div>

            <div class="info-box">
                <div style="font-weight:700; color:#38bdf8; font-size:13px; margin-bottom:8px;">LESION SALIENCY AUDIT</div>
                <table>
                    <thead>
                        <tr style="color:#94a3b8; text-align:left; font-size:11px; text-transform:uppercase;">
                            <th style="padding:6px 12px;">Biomarker Signature</th>
                            <th style="padding:6px 12px;">AI Detection Rationale</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lesion_rows if lesion_rows else "<tr><td colspan='2' style='padding:8px;'>Standard retinal vasculature.</td></tr>"}
                    </tbody>
                </table>
                <p style="font-size:11px; color:#64748b; margin-top:10px;">Attribution Model: {explainability.get('interpretability_method', 'Grad-CAM')} ({explainability.get('feature_layer', 'EfficientNet-B0')})</p>
            </div>
        </div>

        <div class="disclaimer">
            <b>Clinical AI Screening Disclaimer:</b> {settings.MEDICAL_DISCLAIMER}
            <br>
            <i>This algorithmic evaluation is provided as an ophthalmological decision support tool. It does not replace comprehensive dilated clinical examination by a licensed eye care specialist.</i>
        </div>
    </div>
</body>
</html>"""

        html_path = reports_dir / f"{base_name}.html"
        txt_path = reports_dir / f"{base_name}.txt"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"DIABETIC RETINOPATHY EXPLAINABLE AI (XAI) SCREENING REPORT\n")
            f.write(f"Screening ID: {screening_id} | Patient: {patient_id} ({eye})\n")
            f.write(f"Diagnosis: {prediction.get('stage')} (Confidence: {prediction.get('confidence')}%)\n")
            f.write(f"Dominant Attention Quadrant: {explainability.get('dominant_quadrant')}\n")
            f.write(f"Referable DR: {prediction.get('is_referable')}\n")
            f.write(f"Action: {prediction.get('clinical_urgency')}\n")

        return {
            "html_path": str(html_path),
            "txt_path": str(txt_path),
            "html_filename": html_path.name,
        }
