"use client";

import React from "react";
import { PredictionDetail } from "../types/screening";
import { AlertTriangle, CheckCircle2, AlertOctagon, Clock } from "lucide-react";
import { getGradeColor } from "../lib/utils";

interface PredictionCardProps {
  prediction: PredictionDetail;
}

export const PredictionCard: React.FC<PredictionCardProps> = ({ prediction }) => {
  const isReferable = prediction.is_referable;

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-white">Diagnostic Classification</h3>
        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getGradeColor(prediction.grade)}`}>
          Grade {prediction.grade}
        </span>
      </div>

      <div className="mb-4">
        <h2 className="text-2xl font-bold text-white mb-1">{prediction.stage}</h2>
        <div className="flex items-center gap-2">
          <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
              style={{ width: `${prediction.confidence}%` }}
            />
          </div>
          <span className="text-xs font-mono font-bold text-cyan-400">{prediction.confidence}% Conf.</span>
        </div>
      </div>

      <div className="space-y-3 pt-3 border-t border-slate-800/80">
        <div className="flex items-start gap-2.5">
          {isReferable ? (
            <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
          )}
          <div>
            <p className="text-xs font-bold text-slate-200">
              {isReferable ? "Referable DR Detected" : "Non-Referable Presentation"}
            </p>
            <p className="text-xs text-slate-400 mt-0.5">
              {isReferable
                ? "Immediate referral to ophthalmologist or retina specialist recommended."
                : "No vision-threatening microvascular anomalies detected."}
            </p>
          </div>
        </div>

        <div className="flex items-start gap-2.5 bg-slate-950/60 p-3 rounded-xl border border-slate-800">
          <Clock className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-[11px] font-semibold text-cyan-300 uppercase tracking-wide">
              Clinical Action Timeline
            </p>
            <p className="text-xs text-slate-300 mt-0.5 font-medium">
              {prediction.clinical_urgency}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
