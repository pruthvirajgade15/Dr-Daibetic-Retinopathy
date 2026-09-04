"use client";

import React from "react";
import { BarChart3 } from "lucide-react";

interface ConfidenceChartProps {
  probabilities: Record<string, number>;
}

export const ConfidenceChart: React.FC<ConfidenceChartProps> = ({ probabilities }) => {
  const stages = [
    { key: "No DR", label: "0: No DR", color: "bg-emerald-500" },
    { key: "Mild NPDR", label: "1: Mild", color: "bg-cyan-500" },
    { key: "Moderate NPDR", label: "2: Moderate", color: "bg-amber-500" },
    { key: "Severe NPDR", label: "3: Severe", color: "bg-orange-500" },
    { key: "Proliferative DR", label: "4: PDR", color: "bg-red-500" },
  ];

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="w-5 h-5 text-cyan-400" />
        <h3 className="text-base font-semibold text-white">5-Grade Softmax Probabilities</h3>
      </div>

      <div className="space-y-3">
        {stages.map((stage) => {
          const prob = probabilities[stage.key] || probabilities[stage.key.replace(" NPDR", "")] || 0;
          const percentage = Math.round(prob * 100);
          return (
            <div key={stage.key}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-300 font-medium">{stage.label}</span>
                <span className="text-slate-400 font-mono">{percentage}%</span>
              </div>
              <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className={`h-full ${stage.color} rounded-full transition-all duration-500`} style={{ width: `${percentage}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
