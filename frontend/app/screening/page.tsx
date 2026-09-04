"use client";

import React, { useState } from "react";
import { ImageUploader } from "../../components/ImageUploader";
import { ImagePreview } from "../../components/ImagePreview";
import { QualityScore } from "../../components/QualityScore";
import { PredictionCard } from "../../components/PredictionCard";
import { ConfidenceChart } from "../../components/ConfidenceChart";
import { GradCAMViewer } from "../../components/GradCAMViewer";
import { ScreeningReport } from "../../components/ScreeningReport";
import { LoadingState } from "../../components/LoadingState";
import { screeningApi } from "../../lib/api";
import { ScreeningResult } from "../../types/screening";
import { User, Eye, Calendar, Sparkles } from "lucide-react";

export default function ScreeningPage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewSrc, setPreviewSrc] = useState<string | null>(null);
  const [patientId, setPatientId] = useState("PATIENT_1042");
  const [eye, setEye] = useState<"OD" | "OS">("OD");
  const [age, setAge] = useState<number>(58);

  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ScreeningResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelected = (selectedFile: File) => {
    setFile(selectedFile);
    setResult(null);
    setError(null);
    const reader = new FileReader();
    reader.onload = (e) => setPreviewSrc(e.target?.result as string);
    reader.readAsDataURL(selectedFile);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setIsLoading(true);
    setError(null);

    try {
      const data = await screeningApi.screenImage(file, patientId, eye, age);
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to process retinal screening. Ensure backend is running on port 8000.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white">Retinal Screening Studio</h1>
        <p className="text-xs text-slate-400 mt-1">
          Perform multi-modal diagnostic screening with automated IQA, 5-grade staging, and Grad-CAM explainability.
        </p>
      </div>

      {/* Patient Intake Form & Upload */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">Patient Intake</h3>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Patient Identifier</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-9 py-2.5 text-xs text-white focus:outline-none focus:border-cyan-500 font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Eye Laterality</label>
              <select
                value={eye}
                onChange={(e) => setEye(e.target.value as "OD" | "OS")}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="OD">OD (Right Eye)</option>
                <option value="OS">OS (Left Eye)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Patient Age</label>
              <input
                type="number"
                value={age}
                onChange={(e) => setAge(parseInt(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-cyan-500 font-mono"
              />
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!file || isLoading}
            className={`w-full py-3 rounded-xl font-bold text-xs tracking-wide transition-all shadow-lg flex items-center justify-center gap-2 ${
              file && !isLoading
                ? "bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 shadow-cyan-500/20 cursor-pointer"
                : "bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700"
            }`}
          >
            <Sparkles className="w-4 h-4" /> Run AI Retinal Screening
          </button>
        </div>

        <div className="lg:col-span-2">
          {previewSrc ? (
            <div className="space-y-4">
              <ImagePreview imageSrc={previewSrc} patientId={patientId} eye={eye} age={age} />
              <button
                onClick={() => { setFile(null); setPreviewSrc(null); setResult(null); }}
                className="text-xs text-cyan-400 hover:underline"
              >
                ← Upload Different Image
              </button>
            </div>
          ) : (
            <ImageUploader onImageSelected={handleImageSelected} isLoading={isLoading} />
          )}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/40 border border-red-500/30 text-red-400 text-xs font-semibold">
          {error}
        </div>
      )}

      {isLoading && <LoadingState />}

      {result && (
        <div className="space-y-6 pt-4">
          <ScreeningReport
            reportUrl={result.report_download_url}
            patientId={result.patient_id}
            eye={result.eye}
            prediction={result.prediction}
            quality={result.quality}
            explainability={result.explainability}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PredictionCard prediction={result.prediction} />
            <QualityScore quality={result.quality} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <GradCAMViewer images={result.images} explainability={result.explainability} />
            </div>
            <div>
              <ConfidenceChart probabilities={result.prediction.probabilities} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
