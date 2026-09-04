"use client";

import React from "react";
import { Loader2, Eye, Cpu, ShieldCheck } from "lucide-react";

export const LoadingState: React.FC = () => {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-12 text-center backdrop-blur-md flex flex-col items-center justify-center">
      <div className="relative mb-6">
        <div className="w-20 h-20 rounded-full border-4 border-cyan-500/20 border-t-cyan-400 animate-spin flex items-center justify-center" />
        <Eye className="w-8 h-8 text-cyan-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse" />
      </div>

      <h3 className="text-xl font-bold text-white mb-2">Analyzing Retinal Microvasculature...</h3>
      <p className="text-xs text-slate-400 max-w-md mx-auto mb-6">
        Executing image quality checks, Ben Graham color normalization, PyTorch EfficientNet inference, and Grad-CAM attention localization.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-lg text-left">
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 flex items-center gap-2 text-xs text-slate-300">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>IQA Verification</span>
        </div>
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 flex items-center gap-2 text-xs text-slate-300">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>EfficientNet Staging</span>
        </div>
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 flex items-center gap-2 text-xs text-slate-300">
          <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />
          <span>Grad-CAM Saliency</span>
        </div>
      </div>
    </div>
  );
};
