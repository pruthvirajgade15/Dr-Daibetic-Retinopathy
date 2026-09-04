export interface QualityScore {
  overall_quality_score: number;
  sharpness_score: number;
  illumination_score: number;
  contrast_score: number;
  status: string;
  is_gradable: boolean;
}

export interface PredictionDetail {
  grade: number;
  stage: string;
  confidence: number;
  is_referable: boolean;
  clinical_urgency: string;
  probabilities: Record<string, number>;
}

export interface ExplainabilityDetail {
  dominant_quadrant: string;
  quadrants: {
    macula_fovea: number;
    superior_temporal: number;
    inferior_temporal: number;
    superior_nasal: number;
    inferior_nasal: number;
  };
}

export interface MultiModalImages {
  original: string;
  preprocessed: string;
  gradcam: string;
  structures: string;
}

export interface ScreeningResult {
  id: string;
  status: string;
  patient_id: string;
  eye: string;
  age?: number;
  created_at: string;
  quality: QualityScore;
  prediction: PredictionDetail;
  explainability: ExplainabilityDetail;
  images: MultiModalImages;
  report_download_url?: string;
  disclaimer: string;
}

export interface HistoryItem {
  id: string;
  patient_id: string;
  eye: string;
  age?: number;
  predicted_stage: string;
  predicted_grade: number;
  confidence: number;
  is_referable: boolean;
  quality_score: number;
  report_url?: string;
  report_download_url?: string;
  created_at: string;
}

// Aliases for compatibility
export type QualityAssessment = QualityScore;
export type PredictionResult = PredictionDetail;
export type ExplainabilityData = ExplainabilityDetail;
