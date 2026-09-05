import os
import sys
from pathlib import Path
import numpy as np
import torch
import gradio as gr
from PIL import Image

# Ensure root and backend modules are in path
root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

try:
    from backend.app.ml.preprocessing import ben_graham_clahe, segment_vessels_and_disc
    from backend.app.ml.quality_assessment import assess_image_quality
    from backend.app.ml.prediction import predict_stage
    from backend.app.ml.gradcam import generate_gradcam_overlay
except ImportError:
    from app.ml.preprocessing import ben_graham_clahe, segment_vessels_and_disc
    from app.ml.quality_assessment import assess_image_quality
    from app.ml.prediction import predict_stage
    from app.ml.gradcam import generate_gradcam_overlay

# Sample image directory for Gradio gallery/examples
EXAMPLES_DIR = Path(__file__).resolve().parent / "ml-training" / "data" / "processed"
example_images = []
if EXAMPLES_DIR.exists():
    for f in list(EXAMPLES_DIR.glob("*.png"))[:5]:
        example_images.append([str(f)])

def screen_retinal_fundus(input_image):
    if input_image is None:
        return (
            None, None, None, None,
            "Please upload a retinal fundus image to begin screening.",
            {},
            {},
            "N/A", "N/A"
        )

    # Convert to RGB numpy array
    if isinstance(input_image, Image.Image):
        img_np = np.array(input_image.convert("RGB"))
    else:
        img_np = np.array(input_image)

    # 1. Image Quality Assessment
    quality_result = assess_image_quality(img_np)
    
    # 2. Preprocessing (Ben Graham CLAHE)
    prep_np = ben_graham_clahe(img_np, image_size=224)
    
    # 3. Retinal Structure & Vessel Segmentation
    struct_np = segment_vessels_and_disc(img_np)
    
    # 4. Deep Learning Model Inference (5-Grade ICDR)
    prediction_result = predict_stage(img_np)
    grade = prediction_result["grade"]
    stage = prediction_result["stage"]
    confidence = prediction_result["confidence"]
    is_referable = prediction_result["is_referable"]
    urgency = prediction_result["clinical_urgency"]
    probs = prediction_result["probabilities"]
    
    # Format class probabilities for Gradio Label
    confidences = {
        "Grade 0: No DR": probs.get("0", 0.0),
        "Grade 1: Mild DR": probs.get("1", 0.0),
        "Grade 2: Moderate DR": probs.get("2", 0.0),
        "Grade 3: Severe DR": probs.get("3", 0.0),
        "Grade 4: Proliferative DR": probs.get("4", 0.0),
    }

    # 5. Explainable AI: Grad-CAM Heatmap & Quadrant Attribution
    gradcam_np, explain_result = generate_gradcam_overlay(img_np, grade)
    quadrants = explain_result.get("quadrants", {})
    dominant_quadrant = explain_result.get("dominant_quadrant", "Central Macula")
    
    # Format Quadrant Attention for Gradio Label
    quadrant_attention = {
        f"Macula & Fovea": quadrants.get("macula_fovea", 0.0) / 100.0,
        f"Superior Temporal Arcade": quadrants.get("superior_temporal", 0.0) / 100.0,
        f"Inferior Temporal Arcade": quadrants.get("inferior_temporal", 0.0) / 100.0,
        f"Superior Nasal Quadrant": quadrants.get("superior_nasal", 0.0) / 100.0,
        f"Inferior Nasal Quadrant": quadrants.get("inferior_nasal", 0.0) / 100.0,
    }

    # Format Clinical Status Card
    grade_color = "#10b981" if grade == 0 else ("#f59e0b" if grade in (1, 2) else "#ef4444")
    referral_text = "🚨 REFERRAL REQUIRED (Ophthalmology Consultation)" if is_referable else "✅ ROUTINE (Annual Diabetic Eye Exam)"
    
    status_markdown = f"""
### 🩺 Clinical AI Screening Summary
- **Predicted Diagnosis:** <span style="color:{grade_color}; font-size: 1.1em; font-weight: bold;">Grade {grade}: {stage}</span>
- **Model Confidence:** **{confidence}%**
- **Clinical Urgency:** **{urgency}**
- **Referral Action:** **{referral_text}**
- **Image Quality:** **{quality_result['status']}** (Overall Score: {quality_result['overall_quality_score']}/100)
- **Primary Activation Focus:** **{dominant_quadrant}**
    """

    quality_markdown = f"""
| Metric | Score / Status |
| :--- | :--- |
| **Overall Quality** | **{quality_result['overall_quality_score']} / 100** |
| **Focus / Sharpness** | {quality_result['sharpness_score']} / 100 |
| **Illumination Uniformity** | {quality_result['illumination_score']} / 100 |
| **Contrast Clarity** | {quality_result['contrast_score']} / 100 |
| **Gradability Status** | {'✅ Gradable' if quality_result['is_gradable'] else '⚠️ Low Quality'} |
    """

    biomarker_markdown = f"""
| Biomarker Signature | Clinical AI Detection Finding |
| :--- | :--- |
| **Microaneurysms** | {'Detected punctate focal lesions' if grade >= 1 else 'None detected'} |
| **Hard / Soft Exudates** | {'Lipid exudation visible near arcades' if grade >= 2 else 'Unremarkable'} |
| **Retinal Hemorrhages** | {'Dot/blot intraretinal hemorrhages present' if grade >= 2 else 'Unremarkable'} |
| **Neovascularization** | {'Abnormal vessel proliferation active' if grade >= 4 else 'Negative'} |
    """

    return (
        img_np,
        prep_np,
        gradcam_np,
        struct_np,
        status_markdown,
        confidences,
        quadrant_attention,
        quality_markdown,
        biomarker_markdown
    )

# Custom Medical Theme Styling
custom_css = """
.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    max-width: 1200px !important;
    margin: 0 auto !important;
}
.header-box {
    text-align: center;
    padding: 24px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 24px;
}
.disclaimer-box {
    background-color: #451a03;
    border-left: 4px solid #f59e0b;
    padding: 12px 16px;
    border-radius: 8px;
    color: #fde68a;
    font-size: 13px;
    margin-top: 16px;
}
"""

with gr.Blocks(title="DR-Screening-AI | Free Gradio Web App") as demo:
    gr.HTML("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #0b1120 0%, #1e293b 100%); border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin: 0; font-size: 28px; font-weight: 800;">👁️ Diabetic Retinopathy AI Screening & Explainable AI (XAI)</h1>
        <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 14px;">
            Deep Learning (PyTorch EfficientNet-B0) + Automated IQA + Grad-CAM Anatomical Saliency Heatmaps
        </p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            input_img = gr.Image(type="pil", label="Upload Retinal Fundus Image", sources=["upload", "clipboard"])
            run_btn = gr.Button("🔍 Run AI Screening & Diagnostics", variant="primary", size="lg")
            
            if example_images:
                gr.Examples(
                    examples=example_images,
                    inputs=input_img,
                    label="Sample Fundus Images (Click to Test)"
                )

        with gr.Column(scale=1):
            status_output = gr.Markdown("Upload an image and click **Run AI Screening** to view clinical diagnostics.")
            confidence_output = gr.Label(num_top_classes=5, label="5-Grade ICDR Staging Probabilities")

    gr.Markdown("### 🔬 Multi-Modal Computer Vision Diagnostics & Explainable AI")
    with gr.Row():
        orig_view = gr.Image(label="1. Original Fundus", interactive=False)
        prep_view = gr.Image(label="2. Ben Graham CLAHE", interactive=False)
        grad_view = gr.Image(label="3. Grad-CAM Heatmap", interactive=False)
        struct_view = gr.Image(label="4. Vessels & Landmarks", interactive=False)

    with gr.Row():
        with gr.Column():
            quadrant_output = gr.Label(num_top_classes=5, label="Anatomical Quadrant Attention Distribution")
        with gr.Column():
            quality_output = gr.Markdown("### Image Quality Assessment (IQA)\n*Upload image to evaluate.*")
        with gr.Column():
            biomarker_output = gr.Markdown("### Pathological Biomarkers\n*Upload image to evaluate.*")

    gr.HTML("""
    <div style="background-color: #451a03; border-left: 4px solid #f59e0b; padding: 12px 16px; border-radius: 8px; color: #fde68a; font-size: 13px; margin-top: 20px;">
        <b>⚠️ Clinical AI Disclaimer:</b> This system is an AI-assisted diagnostic decision support tool and does not replace professional ophthalmic examination and clinical diagnosis by a licensed eye care specialist.
    </div>
    """)

    run_btn.click(
        fn=screen_retinal_fundus,
        inputs=[input_img],
        outputs=[
            orig_view,
            prep_view,
            grad_view,
            struct_view,
            status_output,
            confidence_output,
            quadrant_output,
            quality_output,
            biomarker_output
        ]
    )

if __name__ == "__main__":
    demo.launch(share=False)
