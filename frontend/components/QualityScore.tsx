"use client";

import React from "react";
import { QualityScore as QualityType } from "../types/screening";
import { ShieldCheck, ShieldAlert, Activity } from "lucide-react";
import { getQualityBadge } from "../lib/utils";

interface QualityScoreProps {
  quality: QualityType;
}

export const QualityScore: React.FC<QualityScoreProps> = ({ quality }) => {
  const badge = getQualityBadge(quality.status);

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-semibold text-white">Image Quality Assessment (IQA)</h3>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${badge.bg} ${badge.text}`}>
          {quality.status}
        </span>
      </div>

      <div className="flex items-baseline gap-2 mb-4">
        <span className="text-3xl font-extrabold text-white">{quality.overall_quality_score}</span>
        <span className="text-xs text-slate-400">/ 100 Clinical Index</span>
      </div>

      <div className="space-y-3">
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Focus & Sharpness</span>
            <span className="text-slate-200 font-mono">{quality.sharpness_score}%</span>
          </div>
          <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-cyan-500 rounded-full" style={{ width: `${quality.sharpness_score}%` }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Illumination Centering</span>
            <span className="text-slate-200 font-mono">{quality.illumination_score}%</span>
          </div>
          <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-blue-500 rounded-full" style={{ width: `${quality.illumination_score}%` }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Contrast & Field of View</span>
            <span className="text-slate-200 font-mono">{quality.contrast_score}%</span>
          </div>
          <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-teal-500 rounded-full" style={{ width: `${quality.contrast_score}%` }} />
          </div>
        </div>
      </div>
    </div>
  );
};
