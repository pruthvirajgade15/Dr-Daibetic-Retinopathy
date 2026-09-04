"use client";

import React from "react";

interface ImagePreviewProps {
  imageSrc: string;
  patientId: string;
  eye: string;
  age?: number;
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({ imageSrc, patientId, eye, age }) => {
  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-white">Input Examination Data</h3>
        <div className="flex gap-2">
          <span className="px-2.5 py-1 rounded bg-slate-800 text-xs font-mono text-cyan-400 border border-slate-700">
            ID: {patientId}
          </span>
          <span className="px-2 py-1 rounded bg-cyan-950 text-xs font-semibold text-cyan-300 border border-cyan-800">
            Eye: {eye}
          </span>
        </div>
      </div>
      <div className="relative aspect-square rounded-xl overflow-hidden bg-black border border-slate-800">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={imageSrc} alt="Retinal Fundus" className="w-full h-full object-contain" />
      </div>
    </div>
  );
};
