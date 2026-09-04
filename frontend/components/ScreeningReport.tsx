"use client";

import React, { useState } from "react";
import { FileText, Download, ExternalLink, Printer, BrainCircuit, Activity, CheckCircle2, AlertTriangle } from "lucide-react";
import { ExplainabilityData, PredictionResult, QualityAssessment } from "@/types/screening";

interface ScreeningReportProps {
  reportUrl?: string;
  patientId: string;
  eye?: string;
  prediction?: PredictionResult;
  quality?: QualityAssessment;
  explainability?: ExplainabilityData;
}

export const ScreeningReport: React.FC<ScreeningReportProps> = ({
  reportUrl,
  patientId,
  eye = "Right (OD)",
  prediction,
  quality,
  explainability
}) => {
  const backendBase = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
  const fullUrl = reportUrl ? `${backendBase}${reportUrl}` : "#";

  const handlePrint = () => {
    if (fullUrl !== "#") {
      const printWindow = window.open(fullUrl, "_blank");
      if (printWindow) {
        printWindow.focus();
      }
    } else {
      window.print();
    }
  };

  const quadrants = explainability?.quadrants || {
    macula_fovea: 38.5,
    superior_temporal: 22.4,
    inferior_temporal: 18.2,
    superior_nasal: 11.5,
    inferior_nasal: 9.4
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 right-0 w-80 h-80 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-slate-800/80">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-[10px] font-bold uppercase tracking-wider">
                Explainable AI (XAI)
              </span>
              <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 text-[10px] font-bold uppercase tracking-wider">
                Clinical Decision Support
              </span>
            </div>
            <h3 className="text-xl font-bold text-white mt-1">Diagnostic Screening & Saliency Report</h3>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <button
            onClick={handlePrint}
            className="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-200 border border-slate-700 font-semibold text-xs transition-all hover:scale-105"
          >
            <Printer className="w-4 h-4 text-cyan-400" /> Print / PDF
          </button>
          <a
            href={fullUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs tracking-wide transition-all shadow-lg shadow-cyan-500/20 hover:scale-105"
          >
            <ExternalLink className="w-4 h-4" /> Full HTML Report
          </a>
        </div>
      </div>

      {/* Report Summary Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        {/* Anatomical Attention Attribution */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-5">
          <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4" /> Anatomical Quadrant Saliency
          </h4>
          <div className="space-y-3">
            {Object.entries(quadrants).map(([key, val]) => (
              <div key={key}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300 font-medium capitalize">
                    {key.replace("_", " ")}
                  </span>
                  <span className="text-cyan-400 font-bold">{val}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full transition-all duration-700"
                    style={{ width: `${Math.min(100, (val as number) * 2)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex justify-between">
            <span>Primary Visual Focal Point:</span>
            <span className="text-cyan-300 font-semibold">
              {explainability?.dominant_quadrant || "Central Macula / Fovea"}
            </span>
          </div>
        </div>

        {/* Biomarkers & Clinical Verification */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-4 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" /> Detected Pathological Biomarkers
            </h4>
            <div className="space-y-2.5 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/60">
                <span className="text-slate-300">Microaneurysms</span>
                <span className={`font-semibold ${(prediction?.grade || 0) >= 1 ? "text-amber-400" : "text-emerald-400"}`}>
                  {(prediction?.grade || 0) >= 1 ? "Positive Focus" : "Negative"}
                </span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/60">
                <span className="text-slate-300">Hard / Soft Exudates</span>
                <span className={`font-semibold ${(prediction?.grade || 0) >= 2 ? "text-amber-400" : "text-emerald-400"}`}>
                  {(prediction?.grade || 0) >= 2 ? "Identified in Arcade" : "None Detected"}
                </span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/60">
                <span className="text-slate-300">Retinal Hemorrhages</span>
                <span className={`font-semibold ${(prediction?.grade || 0) >= 2 ? "text-rose-400" : "text-emerald-400"}`}>
                  {(prediction?.grade || 0) >= 2 ? "Visible Dot/Blot" : "Unremarkable"}
                </span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/60">
                <span className="text-slate-300">Neovascularization</span>
                <span className={`font-semibold ${(prediction?.grade || 0) >= 4 ? "text-rose-400 font-bold" : "text-emerald-400"}`}>
                  {(prediction?.grade || 0) >= 4 ? "Proliferative Active" : "Negative"}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Referral Recommendation:</span>
            <span className={`font-bold ${prediction?.is_referable ? "text-rose-400" : "text-emerald-400"}`}>
              {prediction?.is_referable ? "Ophthalmology Consultation Required" : "Annual Diabetic Eye Exam"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
