# REST API Reference

The FastAPI backend exposes the following RESTful endpoints:

### 1. Health & Readiness Check
- **Endpoint:** `GET /api/health`
- **Response:**
```json
{
  "status": "online",
  "service": "DR-Screening-AI",
  "version": "1.0.0",
  "model_loaded": true,
  "disclaimer": "This system is an AI-assisted screening tool..."
}
```

### 2. Retinal Image Screening
- **Endpoint:** `POST /api/screen`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file`: Fundus Image (`.png`, `.jpg`, `.jpeg`)
  - `patient_id`: String (optional, default `"PATIENT_01"`)
  - `eye`: String (`"OD"` for right eye, `"OS"` for left eye)
  - `age`: Integer (optional)
- **Response:**
  - `quality`: Overall score, sharpness, illumination, usability flag
  - `prediction`: DR grade (0-4), stage name, confidence %, referral urgency, probabilities
  - `explainability`: Dominant focus quadrant, percentage distribution
  - `images`: Base64 encoded Multi-Modal images (Original, Preprocessed, Grad-CAM, Structures)
  - `report_download_url`: Path to generated HTML report

### 3. Screening History
- **Endpoint:** `GET /api/history`
- **Query Params:** `skip=0`, `limit=50`
- **Response:** Array of historical screening records.
