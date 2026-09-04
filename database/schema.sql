-- ==========================================================
-- Explainable AI for Diabetic Retinopathy Screening Database Schema
-- Compatible with SQLite and PostgreSQL
-- ==========================================================

CREATE TABLE IF NOT EXISTS screenings (
    id VARCHAR(36) PRIMARY KEY,
    patient_id VARCHAR(64) NOT NULL,
    patient_hash VARCHAR(64),
    eye VARCHAR(4) DEFAULT 'OD',
    age INTEGER,
    
    -- Retinal Image Quality Assessment (IQA)
    quality_score FLOAT NOT NULL,
    is_gradable BOOLEAN DEFAULT 1,
    quality_status VARCHAR(64) NOT NULL,
    
    -- AI Diagnostic Staging (ICDR 5-Grade Standard)
    predicted_grade INTEGER NOT NULL,
    predicted_stage VARCHAR(64) NOT NULL,
    confidence FLOAT NOT NULL,
    is_referable BOOLEAN DEFAULT 0,
    clinical_urgency VARCHAR(128) NOT NULL,
    probabilities JSON,
    
    -- Explainability & Attention Saliency
    dominant_quadrant VARCHAR(64),
    quadrant_distribution JSON,
    
    -- Clinical Storage
    original_image_path VARCHAR(256),
    report_html_path VARCHAR(256),
    report_txt_path VARCHAR(256),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_screenings_patient ON screenings(patient_id);
CREATE INDEX IF NOT EXISTS idx_screenings_created ON screenings(created_at);
