"use client";

import React, { useState } from "react";
import { UploadCloud, Image as ImageIcon, Sparkles } from "lucide-react";

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
  isLoading: boolean;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({ onImageSelected, isLoading }) => {
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onImageSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onImageSelected(e.target.files[0]);
    }
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
      onDragLeave={() => setIsDragOver(false)}
      onDrop={handleDrop}
      className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all ${
        isDragOver
          ? "border-cyan-400 bg-cyan-950/20 shadow-lg shadow-cyan-500/10"
          : "border-slate-700 hover:border-slate-500 bg-slate-900/50"
      }`}
    >
      <input
        type="file"
        id="fundus-upload"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
        disabled={isLoading}
      />
      <label htmlFor="fundus-upload" className="cursor-pointer flex flex-col items-center gap-3">
        <div className="w-14 h-14 rounded-2xl bg-slate-800/80 border border-slate-700 flex items-center justify-center text-cyan-400 group-hover:scale-105 transition-transform">
          <UploadCloud className="w-7 h-7" />
        </div>
        <div>
          <p className="text-base font-semibold text-white">
            Upload Retinal Fundus Photograph
          </p>
          <p className="text-xs text-slate-400 mt-1">
            Drag and drop PNG, JPG, JPEG, or TIFF (Recommended: Macula-centered 512x512)
          </p>
        </div>
        <span className="mt-2 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/20 transition-all">
          <Sparkles className="w-3.5 h-3.5" /> Select Local File
        </span>
      </label>
    </div>
  );
};
