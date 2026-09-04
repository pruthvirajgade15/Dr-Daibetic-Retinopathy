"use client";

import React, { useState } from "react";
import { MultiModalImages, ExplainabilityDetail } from "../types/screening";
import { Layers, Compass } from "lucide-react";

interface GradCAMViewerProps {
  images: MultiModalImages;
  explainability: ExplainabilityDetail;
}

export const GradCAMViewer: React.FC<GradCAMViewerProps> = ({ images, explainability }) => {
  const [activeTab, setActiveTab] = useState<"gradcam" | "structures" | "preprocessed" | "original">("gradcam");

  const tabs = [
    { id: "gradcam", label: "Grad-CAM Saliency", src: images.gradcam },
    { id: "structures", label: "Vessels & Optic Disc", src: images.structures },
    { id: "preprocessed", label: "Ben Graham CLAHE", src: images.preprocessed },
    { id: "original", label: "Original Fundus", src: images.original },
  ];

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-semibold text-white">Multi-Modal Explainability Studio</h3>
        </div>
        <div className="flex bg-slate-950/80 p-1 rounded-xl border border-slate-800 flex-wrap gap-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === tab.id
                  ? "bg-cyan-500 text-white shadow-md shadow-cyan-500/20"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 relative aspect-square rounded-xl overflow-hidden bg-black border border-slate-800">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={tabs.find((t) => t.id === activeTab)?.src}
            alt="Multi-Modal Retinal View"
            className="w-full h-full object-contain"
          />
        </div>

        <div className="flex flex-col justify-between space-y-4">
          <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
            <div className="flex items-center gap-2 text-cyan-400 mb-2">
              <Compass className="w-4 h-4" />
              <h4 className="text-xs font-bold uppercase tracking-wider">Dominant Saliency Focus</h4>
            </div>
            <p className="text-sm font-semibold text-white">{explainability.dominant_quadrant}</p>
          </div>

          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Quadrant Attention Mass</h4>
            {Object.entries(explainability.quadrants).map(([quad, val]) => (
              <div key={quad}>
                <div className="flex justify-between text-xs mb-0.5">
                  <span className="text-slate-300 capitalize">{quad.replace("_", " ")}</span>
                  <span className="text-slate-400 font-mono">{val}%</span>
                </div>
                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-cyan-500 rounded-full" style={{ width: `${val}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
